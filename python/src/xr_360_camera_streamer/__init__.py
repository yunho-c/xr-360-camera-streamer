"""A Python project that streams 360 panoramic videos to XR headsets."""

from .__about__ import __version__
from .sources.base import VideoSource
from .transforms.base import VideoTransform

__all__ = ["__version__", "VideoSource", "VideoTransform"]
