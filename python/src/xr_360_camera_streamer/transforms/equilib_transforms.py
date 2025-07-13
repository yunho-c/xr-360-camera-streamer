import numpy as np
from equilib import Equi2Pers

from xr_360_camera_streamer.transforms import VideoTransform


class EquilibEqui2Pers(VideoTransform):
    """
    A transform that projects a frame from an equirectangular (360°) source
    to a standard perspective view.

    Args:
        output_width (int): The width of the output perspective video.
        output_height (int): The height of the output perspective video.
    """

    def __init__(self, output_width: int, output_height: int) -> None:
        """
        Initializes the EquilibReprojection.

        Args:
            output_width (int): The width of the output perspective video.
            output_height (int): The height of the output perspective video.
        """
        self._output_width = output_width
        self._output_height = output_height
        self._equi2pers = Equi2Pers(width=output_width, height=output_height)

    @property
    def output_width(self) -> int:
        return self._output_width

    @property
    def output_height(self) -> int:
        return self._output_height

    def transform(self, frame: np.ndarray, rot: dict[str, float], fov_x: float) -> np.ndarray:
        """
        Re-projects an equirectangular frame to a perspective frame.

        Args:
            frame (np.ndarray): The equirectangular frame (H, W, C).
            rot (dict[str, float]): A dictionary with rotation parameters:
                - "pitch": rotation in degrees around the x-axis.
                - "yaw": rotation in degrees around the y-axis.
                - "roll": rotation in degrees around the z-axis.
            fov_x (float): The horizontal field of view in degrees.

        Returns:
            np.ndarray: The perspective frame.
        """
        perspective_frame = self._equi2pers(equi=frame, rot=rot, fov_x=fov_x)
        return perspective_frame
