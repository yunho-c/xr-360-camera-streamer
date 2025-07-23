import asyncio
import json
import os
import time
from pathlib import Path

import numpy as np
from aiortc import MediaStreamTrack
from av import VideoFrame

from xr_360_camera_streamer.sources import FFmpegFileSource, OpenCVFileSource
from xr_360_camera_streamer.streaming import WebRTCServer
from xr_360_camera_streamer.transforms import EquilibEqui2Pers

# Params
VIDEO_SOURCE = FFmpegFileSource
# VIDEO_SOURCE = OpenCVFileSource


# Define a state object for orientation
class AppState:
    def __init__(self):
        self.pitch = 0.0
        self.yaw = 0.0
        self.roll = 0.0
        self.fov_x = 90.0  # Horizontal FOV in degrees

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
        print(f"Received camera data: {data}")
        state.pitch = np.deg2rad(float(data.get("pitch", np.rad2deg(state.pitch))))
        state.yaw = np.deg2rad(float(data.get("yaw", np.rad2deg(state.yaw))))
        state.roll = np.deg2rad(float(data.get("roll", np.rad2deg(state.roll))))
        state.fov_x = float(data.get("fov_x", state.fov_x))
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        print(f"Could not process camera data: {e}")


def on_body_pose_message(message: str):
    try:
        data = json.loads(message)
        print(f"Received pose data: {data}")
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
    data_handlers = {
        "camera": on_camera_message,
        "body_pose": on_body_pose_message,
    }

    server = WebRTCServer(
        video_track_factory=create_video_track,
        datachannel_handlers=data_handlers,
        state_factory=AppState,
    )

    server.run()
