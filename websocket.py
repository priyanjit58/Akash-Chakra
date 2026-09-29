from fastapi import WebSocket


async def broadcast_state(state):

    disconnected = []

    for websocket in connected_clients:

        try:

            await websocket.send_json(
                state
            )

        except Exception:

            disconnected.append(
                websocket
            )

    for websocket in disconnected:

        connected_clients.discard(
            websocket
        )


from api.state import connected_clients