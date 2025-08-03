import asyncio
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame
import sdp_transform

# A dummy video track that produces black frames
class DummyTrack(VideoStreamTrack):
    """
    A video track that returns black frames.
    """
    async def recv(self):
        # Wait for 1/30 of a second to simulate 30fps
        await asyncio.sleep(1/30)
        return VideoFrame(width=640, height=480)

def select_codec(sdp, codec_name):
    """
    Modifies the SDP to use only the specified video codec.
    """
    try:
        sdp_dict = sdp_transform.parse(sdp)

        # Find the video media description
        video_media = next((m for m in sdp_dict["media"] if m["type"] == "video"), None)
        if not video_media:
            return sdp # No video track, do nothing

        # Find the payload type for the desired codec
        rtp_map = next((r for r in video_media["rtp"] if r["codec"].lower() == codec_name.lower()), None)
        if not rtp_map:
            raise ValueError(f"Codec {codec_name} not supported in original offer.")

        payload_type = rtp_map["payload"]

        # Filter all media attributes to keep only the selected codec
        video_media["payloads"] = str(payload_type)
        video_media["rtp"] = [r for r in video_media["rtp"] if r["payload"] == payload_type]
        video_media["fmtp"] = [f for f in video_media["fmtp"] if f["payload"] == payload_type]
        if "rtcpFb" in video_media:
            video_media["rtcpFb"] = [fb for fb in video_media["rtcpFb"] if fb["payload"] == payload_type]

        return sdp_transform.write(sdp_dict)
    except Exception as e:
        print(f"Error modifying SDP: {e}")
        return sdp

async def negotiate_and_check(codec_name):
    """
    Performs a peer-to-peer connection negotiation, forcing a specific codec,
    and checks if the negotiation succeeded.
    """
    print(f"--- 🚀 Attempting to negotiate with {codec_name} ---")

    pc1 = RTCPeerConnection()
    pc2 = RTCPeerConnection()

    # Create an event to signal connection
    connected = asyncio.Event()

    @pc1.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        if pc1.iceConnectionState == "connected":
            connected.set()

    # Add a track to the first peer
    sender = pc1.addTrack(DummyTrack())

    # 1. pc1 creates an offer
    offer = await pc1.createOffer()

    # 2. Modify the offer to only include the desired codec
    modified_sdp = select_codec(offer.sdp, codec_name)
    modified_offer = RTCSessionDescription(sdp=modified_sdp, type=offer.type)

    # 3. pc1 sets its local description, pc2 sets remote
    await pc1.setLocalDescription(modified_offer)
    await pc2.setRemoteDescription(modified_offer)

    # 4. pc2 creates an answer
    answer = await pc2.createAnswer()

    # 5. pc2 sets its local description, pc1 sets remote
    await pc2.setLocalDescription(answer)
    await pc1.setRemoteDescription(answer)

    # Wait for the connection to be established
    try:
        await asyncio.wait_for(connected.wait(), timeout=5.0)
        negotiated_codec = sender.transport.rtp.codec
        print(f"✅ Success! Negotiated Codec: {negotiated_codec.name}")
        print(f"   Payload Type: {negotiated_codec.payloadType}, Clock Rate: {negotiated_codec.clockRate}")
    except asyncio.TimeoutError:
        print(f"❌ Failure! Connection timed out. Could not negotiate {codec_name}.")
    except Exception as e:
        print(f"❌ Failure! An error occurred: {e}")
    finally:
        await pc1.close()
        await pc2.close()
        print("-" * (len(codec_name) + 33))


async def main():
    await negotiate_and_check("VP9")
    await negotiate_and_check("AV1")

if __name__ == "__main__":
    asyncio.run(main())
