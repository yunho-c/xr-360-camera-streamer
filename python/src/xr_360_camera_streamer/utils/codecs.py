from aiortc.codecs import h264, vpx

from .. import logger


def maybe_enable_hardware_acceleration():
    """
    Monkey-patches the H264 and VP8 encoders to use hardware acceleration if
    available.

    This function checks for the presence of NVIDIA, Intel Quick Sync (QSV),
    or macOS VideoToolbox hardware encoders and replaces the default software
    encoders in `aiortc` with the first one it finds for each codec.
    """
    # H.264
    if hasattr(h264, "H264NvencEncoder"):
        logger.info("H.264: Using NVIDIA NVENC hardware acceleration.")
        h264.H264Encoder = h264.H264NvencEncoder
    elif hasattr(h264, "H264QsvEncoder"):
        logger.info("H.264: Using Intel QSV hardware acceleration.")
        h264.H264Encoder = h264.H264QsvEncoder
    elif hasattr(h264, "H264VideotoolboxEncoder"):
        logger.info("H.264: Using macOS VideoToolbox hardware acceleration.")
        h264.H264Encoder = h264.H264VideotoolboxEncoder
    else:
        logger.warning(
            "H.264: No hardware acceleration available, falling back to software encoder."
        )

    # VP8
    if hasattr(vpx, "Vp8NvencEncoder"):
        logger.info("VP8: Using NVIDIA NVENC hardware acceleration.")
        vpx.Vp8Encoder = vpx.Vp8NvencEncoder
    elif hasattr(vpx, "Vp8QsvEncoder"):
        logger.info("VP8: Using Intel QSV hardware acceleration.")
        vpx.Vp8Encoder = vpx.Vp8QsvEncoder
    else:
        logger.warning("VP8: No hardware acceleration available, falling back to software encoder.")
