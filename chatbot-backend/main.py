
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Cookie, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from v1.src.session import SessionManager
from v1.src.flows import Flow
from core.settings import settings
from fastapi.staticfiles import StaticFiles
from v1 import v1
from core.models.chat_message_model import ApplicationData
from v1.src.logger import logger


origins = settings.api.ORIGINS


api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Access-Control-Allow-Origin"],  # You can restrict headers to specific ones if needed
    expose_headers=["*"],

)

api.mount("/editor", StaticFiles(directory="static", html=True), name="static")
api.include_router(v1.router)


html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Chat</title>
        </head>
        <body>
            <h1>WebSocket Chat</h1>
            <h2>Your ID: <span id="ws-id"></span></h2>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id='messages' markdown="span">
            </ul>
            <script>
                var session_id = Date.now()
                document.querySelector("#ws-id").textContent = session_id;
                var ws = new WebSocket(`ws://localhost:8000/ws/tenantev/${session_id}`);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                function sendMessage(event) {
                    var input = document.getElementById("messageText")
                    var jsonData = JSON.stringify({"text": input.value})
                    ws.send(jsonData)
                    input.value = ''
                    event.preventDefault()
                }
            </script>
        </body>
    </html>
    """





manager = SessionManager()

@api.get("/")
async def get():
    return HTMLResponse(html)


@api.put("/{session_id}/data")
async def update_session(session_id: str,
                         data:ApplicationData, token:str = Cookie()):
    data = data.model_dump(by_alias=True)
    data["token"] = token
    try:
        await manager.add_application_data(session_id=session_id, data=data)
        return {"message": "Session updated"}
    except Exception:
        raise HTTPException(status_code=404, detail="Session not found")
    

@api.websocket("/ws/{origin}/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    origin: str,
    session_id: str, 
    user_agent: str | None = Header(None)):
    await websocket.accept()
    flow = Flow.from_json()
    graph = flow.graph
    user_session = manager.create_session(session_id=session_id, graph=graph,origin=origin)
    user_session.tracker["user_agent"] = user_agent
    
    
    try:
        await user_session.start_flow(websocket)
        await manager.save(session_id)
    except WebSocketDisconnect as e:
        logger.error(e)
        await manager.save(session_id)
    except Exception as e:
        logger.error(e)
        await manager.save(session_id)
        
    finally:
        # TODO Save session to db
        await manager.delete_session(session_id)
        logger.info(f"Session ended for {session_id}")
        
    
