import subprocess
from pathlib import Path

import cv2
import numpy as np

from xr_360_camera_streamer.sources import VideoSource


class FFmpegFileSource(VideoSource):
    """
    A video source that reads from a file using a direct FFmpeg subprocess pipe.

    This can be faster for some high-resolution or high-framerate videos
    as it avoids some of the overhead of OpenCV's wrapper.

    Requires `ffmpeg` to be installed and accessible in the system's PATH.

    Args:
        filepath (str): The path to the video file.
    """

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        if not self.filepath.is_file():
            raise FileNotFoundError(f"Video file not found at: {filepath}")

        # Use OpenCV once to get reliable metadata.
        # This is simpler than parsing ffprobe's output.
        cap = cv2.VideoCapture(str(self.filepath))
        if not cap.isOpened():
            raise ValueError(f"Failed to open video file with OpenCV (to get metadata): {filepath}")

        self._width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        # Calculate the size of a single frame in bytes (Width x Height x 3 channels for RGB)
        self.frame_size = self._width * self._height * 3

        # Construct the FFmpeg command
        # fmt: off
        self.ffmpeg_command = [
            'ffmpeg',                 # Input file
            '-i', str(self.filepath), # Suppress verbose output
            '-loglevel', 'error',     # Output format: raw video frames
            '-f', 'rawvideo',         # Pixel format: 24-bit RGB
            '-pix_fmt', 'rgb24',      # Output to stdout
            '-'
        ]
        # fmt: on

        # Start the FFmpeg subprocess
        self.process = subprocess.Popen(
            self.ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def fps(self) -> float:
        return self._fps

    def __next__(self) -> np.ndarray:
        """Reads a raw frame from the stdout pipe and reshapes it."""
        # Read the exact number of bytes for one frame
        raw_frame = self.process.stdout.read(self.frame_size)

        if len(raw_frame) != self.frame_size:
            # End of stream or error
            self.release()
            raise StopIteration

        # Reshape the raw byte buffer into a NumPy array (H, W, C)
        frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.height, self.width, 3))
        return frame

    def release(self):
        """Terminates the FFmpeg subprocess and closes pipes."""
        if hasattr(self, "process") and self.process.poll() is None:
            self.process.terminate()
            # Wait for the process to terminate to avoid zombie processes
            try:
                self.process.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                self.process.kill()
