"""A Python project that streams 360 panoramic videos to XR headsets."""

from loguru import logger

from . import __about__
from .logging import configure_logging
from .sources.base import VideoSource
from .transforms.base import VideoTransform

__all__ = [
    "__version__",
    "logger",
    "configure_logging",
    "VideoSource",
    "VideoTransform",
]
__version__ = __about__.version

# Set up default logging for the library.
# Users can easily override this by calling `configure_logging()` with their
# preferred settings.
configure_logging()
