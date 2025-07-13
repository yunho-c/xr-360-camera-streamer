"""Command-line interface for xr-360-camera-streamer."""

import sys

from . import logger


def main() -> int:
    """The main function of the command-line interface."""
    logger.info("Starting XR 360 Camera Streamer...")
    # Your application logic will go here
    return 0


if __name__ == "__main__":
    sys.exit(main())
