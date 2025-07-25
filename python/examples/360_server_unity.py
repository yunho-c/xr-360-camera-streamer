import argparse
import asyncio
import json
import os
import time
from functools import partial
from pathlib import Path
from typing import Any, Optional

import numpy as np
from aiortc import MediaStreamTrack
from av import VideoFrame

from xr_360_camera_streamer.sources import FFmpegFileSource, OpenCVFileSource
from xr_360_camera_streamer.streaming import WebRTCServer
from xr_360_camera_streamer.transforms import EquilibEqui2Pers

# Params
# video source library
VIDEO_SOURCE = FFmpegFileSource
# VIDEO_SOURCE = OpenCVFileSource

# body pose visualization
VISUALIZE = True
# VISUALIZE = False


# Define a state object for orientation
class AppState:
    def __init__(self, visualizer: Optional[Any] = None):
        self.pitch = 0.0
        self.yaw = 0.0
        self.roll = 0.0
        self.fov_x = 90.0  # Horizontal FOV in degrees
        self.visualizer = visualizer

    def __repr__(self):
        return (
            f"<AppState pitch={self.pitch}, yaw={self.yaw}, roll={self.roll}, fov_x={self.fov_x}>"
        )

    def get_rot(self) -> dict[str, float]:
        return {"pitch": self.pitch, "yaw": self.yaw, "roll": self.roll}


# Define a custom video track that applies reprojection
class ReprojectionTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, state: AppState, source: VIDEO_SOURCE, transform: EquilibEqui2Pers):
        super().__init__()
        self.state = state
        self.source = source
        self.transform = transform
        self._timestamp = 0

    async def recv(self):
        equi_frame_rgb = next(self.source)  # ALT

        # Get current orientation from the shared state
        rot = self.state.get_rot()

        # # Apply the equirectangular-to-perspective transform
        perspective_frame = self.transform.transform(frame=equi_frame_rgb, rot=rot)

        # Create a VideoFrame for aiortc
        frame = VideoFrame.from_ndarray(perspective_frame, format="rgb24")

        # Set timestamp
        time_base = 90000
        frame.pts = self._timestamp
        frame.time_base = time_base
        self._timestamp += int(time_base / self.source.fps)

        return frame


# Data channel handler to update orientation state
def on_camera_message(message: str, state: AppState):
    try:
        data = json.loads(message)
        # print(f"Received camera data: {data}")
        state.pitch = np.deg2rad(float(data.get("pitch", np.rad2deg(state.pitch))))
        state.yaw = np.deg2rad(float(data.get("yaw", np.rad2deg(state.yaw))))
        state.roll = np.deg2rad(float(data.get("roll", np.rad2deg(state.roll))))
        state.fov_x = float(data.get("fov_x", state.fov_x))
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        print(f"Could not process camera data: {e}")


def on_body_pose_message(message: str, state: AppState):
    try:
        data = json.loads(message)
        print(f"Received pose data: {data}")

        # Log to rerun
        if state.visualizer:
            rr = state.visualizer
            # https://rerun.io/docs/concepts/timelines
            rr.set_time("body_pose_timestamp", timestamp=data["timestamp"])
            for bone in data["bones"]:
                rr.log(
                    f"world/user/bones/{bone['id']}",
                    rr.Points3D(positions=[list(bone["position"].values())]), # parse dict to list
                )

    except (json.JSONDecodeError, TypeError, ValueError) as e:
        print(f"Could not process body pose data: {e}")


# Factory for creating the video track
def create_video_track(state: AppState):
    video_path = os.path.join(
        Path(__file__).parents[2],
        "xr-360-streamer-assets",
        "videos",
        "test_video.mp4",
    )

    if not os.path.exists(video_path):
        raise FileNotFoundError(
            f"Video asset not found at {video_path}. "
            "Please download the assets from the repository "
            "and place them in `xr-360-streamer-assets` at the project root."
        )

    # Initialize the video source and transform
    video_source = VIDEO_SOURCE(video_path)
    video_transform = EquilibEqui2Pers(output_width=1280, output_height=720, fov_x=state.fov_x)

    return ReprojectionTrack(state, video_source, video_transform)


# Start server
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XR 360 Camera Streamer")
    parser.add_argument(
        "--visualize", action="store_true", help="Enable 3D visualization with rerun."
    )
    args = parser.parse_args()

    rr = None
    state_factory = AppState
    if VISUALIZE or args.visualize:
        try:
            import rerun as rr
        except ImportError:
            print("Please install rerun SDK: pip install -e .[viz]")
            exit(1)

        rr.init("xr-360-camera-streamer", spawn=True)
        state_factory = partial(AppState, visualizer=rr)

    data_handlers = {
        "camera": on_camera_message,
        "body_pose": on_body_pose_message,
    }

    server = WebRTCServer(
        video_track_factory=create_video_track,
        datachannel_handlers=data_handlers,
        state_factory=state_factory,
    )

    server.run()
