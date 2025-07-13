import asyncio
import logging
import uuid
from contextlib import asynccontextmanager

import uvicorn
from aiortc import RTCPeerConnection, RTCSessionDescription
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebRTCServer:
    """
    A reusable WebRTC server that allows customization of video tracks,
    data channel message handlers, and a shared state object per peer.
    """

    def __init__(
        self,
        host="0.0.0.0",
        port=8080,
        video_track_factory=None,
        datachannel_handlers=None,
        state_factory=None,
        html_template=None,
    ):
        """
        Initializes the WebRTC Server.

        NOTE: Both `video_track_factory` and `datachannel_handlers` must have function
              signatures that accept `state` as a keyword argument.

        Args:
            host (str, optional): The host to bind the server to. Defaults to "0.0.0.0".
            port (int, optional): The port to run the server on. Defaults to 8080.
            video_track_factory (callable, optional): A function or class that, when called,
                returns a new instance of a MediaStreamTrack. It will receive a `state` object
                as a keyword argument.
            datachannel_handlers (dict, optional): A dictionary mappping data channel labels
                (str) to callback functions. Callbacks will receive the message and a `state`
                object as keyword arguments.
            state_factory (callable, optional): A function or class that, when called, returns
                a new state object for the peer connection.
        """
        self.host = host
        self.port = port
        self.video_track_factory = video_track_factory
        self.datachannel_handlers = datachannel_handlers
        self.state_factory = state_factory
        self.app = FastAPI(lifespan=self.lifespan)
        self.pcs = set()  # global storage for peer connection(s)

        self.app.post("/offer")(self._create_offer_handler)  # WebRTC signal endpoint
        if html_template:
            self.html_template = html_template
            self.templates = Jinja2Templates(directory="templates")
            self.app.mount("/static", StaticFiles(directory="static"), name="static")
            self.app.get("/", response_class=HTMLResponse)(self.index)  # root endpoint to serve the HTML page

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        # Startup
        yield

        # Shutdown
        logger.info("Server shutting down, closing all peer connections.")
        # Make a copy of the set to iterate over, as closing pcs modifies the set
        coros = [pc.close() for pc in list(self.pcs)]
        await asyncio.gather(*coros)
        self.pcs.clear()

    async def _create_offer_handler(self, request: Request):
        """
        Handles the SDP offer from the client and returns an SDP answer.
        """
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

        # Create a new peer connection
        pc = RTCPeerConnection()
        pc_id = f"PeerConnection({uuid.uuid4()})"
        self.pcs.add(pc)
        logger.info(f"{pc_id}: Created for {request.client.host}")

        # Create a state object for peer connection
        state = self.state_factory()
        logger.info(f"{pc_id}: Created state object: {state}")

        # Create a video track for peer connection
        if self.video_track_factory:
            logger.info(f"{pc_id}: Creating video track using provided factory.")
            video_track = self.video_track_factory(state=state)
            pc.addTrack(video_track)
        else:
            logger.warning(f"{pc_id}: No video_track_factory provided.")

        # Create a data channel handler
        @pc.on("datachannel")
        def on_datachannel(channel):
            label = channel.label
            logger.info(f"{pc_id}: Data channel '{label}' created.")

            if label in self.datachannel_handlers:
                handler = self.datachannel_handlers[label]

                @channel.on("message")
                async def on_message(message):
                    logger.info(f"{pc_id}: Message on '{label}': {message}")
                    handler(message=message, state=state)
            else:
                logger.warning(f"{pc_id}: No handler registered for data channel '{label}'.")

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            logger.info(f"{pc_id}: Connection state is {pc.connectionState}")
            if pc.connectionState in ("failed", "closed", "disconnected"):
                await pc.close()
                self.pcs.discard(pc)
                logger.info(f"{pc_id}: Cleaned up.")

        try:
            await pc.setRemoteDescription(offer)
            answer = await pc.createAnswer()
            await pc.setLocalDescription(answer)

        except Exception as e:
            logger.error(f"{pc_id}: Error during offer/answer exchange: {e}")
            await pc.close()
            self.pcs.discard(pc)
            return JSONResponse(status_code=500, content={"error": str(e)})

        # Return the answer to the client
        return JSONResponse(
            content={"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        )

    async def index(self, request: Request):
        return self.templates.TemplateResponse(self.html_template, {"request": request})

    def run(self):
        """Starts the web server."""
        logger.info(f"Starting server on http://{self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=self.port)
