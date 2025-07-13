import asyncio
import json
import os
import time
from pathlib import Path

import numpy as np
from aiortc import MediaStreamTrack
from av import VideoFrame
from fastapi.responses import FileResponse

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

        # ORIG
        # try:
        #     # Get the next equirectangular frame from the source
        #     equi_frame_rgb = next(self.source)
        # except StopIteration:
        #     # Loop the video (or handle end-of-stream)
        #     print("Restarting video source...")
        #     # This is a simple way to loop. A more robust solution might be needed.
        #     self.source.release()
        #     self.source = VIDEO_SOURCE(self.source.filepath)
        #     equi_frame_rgb = next(self.source)

        # Get current orientation from the shared state
        rot = self.state.get_rot()
        # fov_x = self.state.fov_x

        # # Apply the equirectangular-to-perspective transform
        perspective_frame = self.transform.transform(frame=equi_frame_rgb, rot=rot)
        # perspective_frame = equi_frame_rgb  # DEBUG

        # Create a VideoFrame for aiortc
        frame = VideoFrame.from_ndarray(perspective_frame, format="rgb24")

        # Set timestamp
        time_base = 90000
        frame.pts = self._timestamp
        frame.time_base = time_base
        self._timestamp += int(time_base / self.source.fps)

        return frame


# Data channel handler to update orientation state
def on_control_message(message: str, state: AppState):
    try:
        data = json.loads(message)
        print(f"Received control data: {data}")
        state.pitch = np.deg2rad(float(data.get("pitch", state.pitch)))
        state.yaw = np.deg2rad(float(data.get("yaw", state.yaw)))
        state.roll = np.deg2rad(float(data.get("roll", state.roll)))
        state.fov_x = float(data.get("fov_x", state.fov_x))
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        print(f"Could not process control command: {e}")


# Factory for creating the video track
def create_video_track(state: AppState):
    # NOTE: Update this path to your 360 video file.
    # The asset directory is expected to be at the root of the repository.
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
        "control": on_control_message,
    }

    server = WebRTCServer(
        video_track_factory=create_video_track,
        datachannel_handlers=data_handlers,
        state_factory=AppState,
    )

    # Serve frontend HTML file
    @server.app.get("/")
    async def read_root():
        return FileResponse(os.path.join(os.path.dirname(__file__), "360_server_reprojection.html"))

    server.run()
