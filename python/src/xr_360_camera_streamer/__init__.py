"""A Python project that streams 360 panoramic videos to XR headsets."""

import logging

from . import __about__
from .sources.base import VideoSource
from .transforms.base import VideoTransform

__all__ = ["__version__", "VideoSource", "VideoTransform"]
__version__ = __about__.version

# Set up logging for the library.
# This will create a default handler that logs to the console.
# If the user of the library has configured logging, this will not run,
# and the library will use the user's logging configuration.
logger = logging.getLogger(__name__)
if not logging.getLogger().handlers:
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
