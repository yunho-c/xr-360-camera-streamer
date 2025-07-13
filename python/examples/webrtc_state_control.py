import asyncio
import json
import os
import time
from datetime import datetime

from aiortc import MediaStreamTrack
from av import VideoFrame
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw, ImageFont

from xr_360_camera_streamer.streaming import WebRTCServer


# Define a state object
class AppState:
    def __init__(self):
        # Default color for the video text
        self.text_color = "white"

    def __repr__(self):
        return f"<AppState text_color='{self.text_color}'>"


# Define a custom video track
class CustomTimeTrack(MediaStreamTrack):
    """
    A custom video track that reads from the shared state object
    to determine the color of the text it draws.
    """

    kind = "video"

    def __init__(self, state: AppState):
        super().__init__()
        # Store the state object for this connection
        self.state = state
        self.last_frame_time = 0
        self.frame_rate = 30
        self._timestamp = 0
        try:
            self.font = ImageFont.truetype("arial.ttf", 24)
        except OSError:
            self.font = ImageFont.load_default()

    async def recv(self):
        now = time.time()
        await asyncio.sleep(max(0, (self.last_frame_time + 1.0 / self.frame_rate) - now))
        self.last_frame_time = time.time()

        img = Image.new("RGB", (640, 480), color="black")
        draw = ImageDraw.Draw(img)
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        # Read from the state object
        color = self.state.text_color

        # NOTE: The color is now determined by the shared state, which
        # can be changed by the data channel handler.
        draw.text((100, 220), current_time_str, font=self.font, fill=color)

        frame = VideoFrame.from_image(img)

        time_base = 90000
        frame.pts = self._timestamp
        frame.time_base = time_base
        self._timestamp += int(time_base / self.frame_rate)

        return frame


# Define custom data channel callbacks (to use the state)
def on_chat_message(message: str, state: AppState):
    """Callback for the 'chat' data channel."""
    print(f"Received chat message: '{message}' (Current state: {state})")


def on_control_message(message: str, state: AppState):
    """
    Callback for the 'control' data channel. This handler will
    modify the shared state object.
    """
    print(f"Received control command: '{message}'")
    try:
        data = json.loads(message)
        if data.get("command") == "set_color":
            new_color = data.get("value", "white")
            print(f"Changing text color to '{new_color}' for state: {state}")

            # Write to the state object
            state.text_color = new_color

    except Exception as e:
        print(f"Could not process control command: {e}")


# Start server
if __name__ == "__main__":
    data_handlers = {
        "chat": on_chat_message,
        "control": on_control_message,
    }

    server = WebRTCServer(
        video_track_factory=CustomTimeTrack,  # (must accept 'state' )
        datachannel_handlers=data_handlers,  # (must accept 'message' and 'state')
        state_factory=AppState,
    )

    # serve frontend HTML file
    @server.app.get("/")
    async def read_root():
        return FileResponse(os.path.join(os.path.dirname(__file__), "webrtc_state_control.html"))

    server.run()
