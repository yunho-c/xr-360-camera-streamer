import asyncio
import os
import time

from aiortc import MediaStreamTrack
from av import VideoFrame
from fastapi.responses import FileResponse

from xr_360_camera_streamer.sources import FFmpegFileSource
from xr_360_camera_streamer.streaming import WebRTCServer


# Define a simple video track that streams a file
class VideoFileTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, source: FFmpegFileSource):
        super().__init__()
        self.source = source
        self._timestamp = 0

    async def recv(self):
        try:
            # Get the next frame from the source
            frame_rgb = next(self.source)
        except StopIteration:
            # Loop the video
            print("Restarting video source...")
            self.source.release()
            self.source = FFmpegFileSource(self.source.filepath)
            frame_rgb = next(self.source)

        # Create a VideoFrame for aiortc
        frame = VideoFrame.from_ndarray(frame_rgb, format="rgb24")

        # Set timestamp
        time_base = 90000
        frame.pts = self._timestamp
        frame.time_base = time_base
        self._timestamp += int(time_base / self.source.fps)

        return frame


# Factory for creating the video track
def create_video_track():
    # NOTE: Update this path to your video file.
    # The asset directory is expected to be at the root of the repository.
    video_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "xr-360-streamer-assets",
        "videos",
        "360_video.mp4",  # Using the same video, but without reprojection
    )

    if not os.path.exists(video_path):
        raise FileNotFoundError(
            f"Video asset not found at {video_path}. "
            "Please download the assets from the repository "
            "and place them in `xr-360-streamer-assets` at the project root."
        )

    # Initialize the video source
    video_source = FFmpegFileSource(video_path, hw_accel_enabled=True)
    return VideoFileTrack(video_source)


# Start server
if __name__ == "__main__":
    # No state or data channels needed for this simple example
    server = WebRTCServer(
        video_track_factory=create_video_track,
    )

    # Serve frontend HTML file
    @server.app.get("/")
    async def read_root():
        return FileResponse(os.path.join(os.path.dirname(__file__), "basic_video_stream.html"))

    server.run()
