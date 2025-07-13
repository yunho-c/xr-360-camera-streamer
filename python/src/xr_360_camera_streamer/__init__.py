"""A Python project that streams 360 panoramic videos to XR headsets."""

from . import __about__
from .sources.base import VideoSource
from .transforms.base import VideoTransform

__all__ = ["__version__", "VideoSource", "VideoTransform"]
__version__ = __about__.version
