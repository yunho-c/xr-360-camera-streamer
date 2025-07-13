import asyncio
import logging
import uuid
from contextlib import asynccontextmanager

from aiortc import RTCPeerConnection, RTCSessionDescription
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global storage for peer connection(s)
pcs = set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    logger.info("Server shutting down, closing all peer connections.")
    # Make a copy of the set to iterate over, as closing pcs modifies the set
    coros = [pc.close() for pc in list(pcs)]
    await asyncio.gather(*coros)
    pcs.clear()


# FastAPI setup
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Root endpoint to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Signaling endpoint for WebRTC
@app.post("/offer")
async def offer(request: Request):
    """
    Handles the SDP offer from the client and returns an SDP answer.
    """
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    # Create a new peer connection
    pc = RTCPeerConnection()
    pc_id = f"PeerConnection({uuid.uuid4()})"
    pcs.add(pc)

    logger.info(f"{pc_id}: Created for {request.client.host}")

    # Add video track
    video_track = None  # TODO
    pc.addTrack(video_track)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        logger.info(f"{pc_id}: Connection state is {pc.connectionState}")
        if pc.connectionState == "failed" or pc.connectionState == "closed":
            await pc.close()
            pcs.discard(pc)
            logger.info(f"{pc_id}: Closed and removed.")

    try:
        await pc.setRemoteDescription(offer)

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

    except Exception as e:
        logger.error(f"Error during offer/answer exchange: {e}")
        await pc.close()
        pcs.discard(pc)
        return JSONResponse(status_code=500, content={"error": str(e)})

    # Return the answer to the client
    return JSONResponse(content={"sdp": pc.localDescription.sdp, "type": pc.localDescription.type})
