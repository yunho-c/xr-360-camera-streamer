import av

def check_codec(name, mode='r'):
    """
    Checks if a codec is available for a given mode.
    'r' for decoder, 'w' for encoder.
    """
    try:
        # Try to get the codec from the registry
        codec = av.codec.Codec(name, mode)
        print(f"✅ Success: Codec '{name}' ({'decoder' if mode == 'r' else 'encoder'}) is available.")
        return True
    except av.error.ValueError:
        # This error is raised if the codec is not found
        print(f"❌ Failure: Codec '{name}' ({'decoder' if mode == 'r' else 'encoder'}) is NOT available.")
        return False

print("--- Testing Codec Initialization ---")
# Test for decoders ('r' mode)
check_codec('av1', 'r')      # Generic AV1 decoder
check_codec('libdav1d', 'r') # Specific high-performance AV1 decoder
check_codec('vp9', 'r')      # VP9 decoder

print("\n--- Testing Encoders ---")
# Test for encoders ('w' mode)
check_codec('libaom-av1', 'w') # AV1 encoder
check_codec('libvpx-vp9', 'w') # VP9 encoder
