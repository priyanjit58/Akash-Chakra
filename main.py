import asyncio

from fastapi import (
    FastAPI,
    WebSocket,
    HTTPException
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.responses import (
    FileResponse
)

from api.state import engine
from api.websocket import (
    connected_clients,
    broadcast_state
)


app = FastAPI(
    title="AKASH CHAKRA",
    description="BAPS Spectrum Simulation API",
    version="1.0.0"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# =====================================================
# STARTUP
# =====================================================

@app.on_event("startup")
async def startup():

    asyncio.create_task(

        engine.run_loop(
            broadcast_state
        )
    )


# =====================================================
# ROOT
# =====================================================

@app.get("/")
async def root():

    return FileResponse(
        "dashboard/index.html"
    )


# =====================================================
# CURRENT STATE
# =====================================================

@app.get("/api/state")
async def get_state():

    return engine.get_state()


# =====================================================
# START
# =====================================================

@app.post("/api/start")
async def start():

    engine.running = True

    return {
        "status": "running"
    }


# =====================================================
# STOP
# =====================================================

@app.post("/api/stop")
async def stop():

    engine.running = False

    return {
        "status": "stopped"
    }


# =====================================================
# RESET
# =====================================================

@app.post("/api/reset")
async def reset():

    engine.running = False

    engine.reset()

    return engine.get_state()


# =====================================================
# POLICY
# =====================================================

@app.post("/api/policy/{policy}")
async def change_policy(
    policy: str
):

    try:

        engine.set_policy(
            policy
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "policy":
            engine.policy
    }


# =====================================================
# DWELL
# =====================================================

@app.post("/api/dwell/{value}")
async def change_dwell(
    value: float
):

    if value <= 0:

        raise HTTPException(
            status_code=400,
            detail="Dwell must be positive"
        )

    engine.dwell_time = value

    return {
        "dwell":
            engine.dwell_time
    }


# =====================================================
# SPEED
# =====================================================

@app.post("/api/speed/{value}")
async def change_speed(
    value: float
):

    engine.speed = max(
        0.1,
        min(10.0, value)
    )

    return {
        "speed":
            engine.speed
    }


# =====================================================
# WEBSOCKET
# =====================================================

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    connected_clients.add(
        websocket
    )

    # Send immediate state
    await websocket.send_json(
        engine.get_state()
    )

    try:

        while True:

            await websocket.receive_text()

    except Exception:

        pass

    finally:

        connected_clients.discard(
            websocket
        )