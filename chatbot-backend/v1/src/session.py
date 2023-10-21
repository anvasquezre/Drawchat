from fastapi import WebSocket, HTTPException
import networkx as nx
from typing import Dict, Any, Optional,List, ClassVar

from core.models.base_model import generate_date_str
from ..utils.utils import generate_uuid
from pydantic import BaseModel, Field
from core.models.chat_message_model import ChatMessage, Elements
import asyncio as aio
from core.models.chatlog_models import MessageCreate, SessionCreate
from core.settings import settings
import requests
from v1.src.logger import logger
class Session(BaseModel): 
    starter_node: ClassVar[str] = "start00000000"
    tracker: Dict[str, Any] = {}
    session_id: Optional[str] = Field(default_factory=generate_uuid)
    graph: Optional[nx.DiGraph] = None
    origin: Optional[str] = None
    class Config:
        arbitrary_types_allowed = True
    
    def get_next_node(self, current_node: str, intent:Optional[str | None] = None) -> str:
        next_nodes = [node for node in self.graph.neighbors(current_node)]
        if len(next_nodes) == 1:
            next_node = next_nodes[0]
        elif len(next_nodes) > 1:
            for node in next_nodes:
                if self.graph.nodes[node]["handler"].label == intent:
                    next_node = node
                    break

        elif len(next_nodes) == 0:
            next_node = None
        self.tracker["current_node"] = next_node
        
        

    async def execute(
        self,
        value: str,
        keys: Optional[List[str]] = None,
        current_node: Optional[str] = None,
        ) -> Any:
        
        node_name = current_node
        current_node = self.graph.nodes[node_name]
        data,intent = current_node["handler"](value,self.tracker)
        for key in keys:
            self.tracker[key] = data
            
        try:
            self.get_next_node(current_node=node_name,intent=intent)
        except Exception as e:
            print(e)
            self.tracker["current_node"] = None
            return "No intent found"
        

        return data

    async def handle_listen_node(
        self, 
        websocket: WebSocket,
        keys: List[str], 
        element_list: List[Elements], 
        feedback:bool,
        current_node:str,
        timeout:int
        ):
        try:
            session_id = self.session_id
            # Send Listen Signal to UI to allow user to send message
            message = ChatMessage(
                message_id=None,
                text=None,
                elements=element_list,
                user="listen_signal",
                session_id=session_id,
                feedback=feedback
            )
            self.tracker["history"].append(message.model_dump(by_alias=True))
            await websocket.send_json(message.model_dump(by_alias=True))

            # Waits for user message for timeout seconds
            response = await aio.wait_for(websocket.receive_json(), timeout=timeout)   
            value = response["text"]
            text = await self.execute(value=value, keys=keys, current_node=current_node)
            message = ChatMessage(
                text=text,
                elements=None,
                user="USER",
                session_id=session_id,
                feedback=feedback
            )
            self.tracker["history"].append(message.model_dump(by_alias=True))
            await websocket.send_json(message.model_dump(by_alias=True))

            message = ChatMessage(
                message_id=None,
                text=None,
                elements=None,
                user="ai_signal",
                session_id=session_id,
                feedback=feedback
            )
            self.tracker["history"].append(message.model_dump(by_alias=True))
            await websocket.send_json(message.model_dump(by_alias=True))
            self.tracker["timeout_iters"] = 0
        except aio.TimeoutError:
            # if timeout, send timeout message and set value to None
            if self.tracker["timeout_iters"] >= 1:
                message = ChatMessage(
                message_id=None,
                text=None,
                elements=None,
                user="timeout_signal",
                session_id=session_id,
                feedback=feedback
                )
                self.tracker["history"].append(message.model_dump(by_alias=True))
                await websocket.send_json(message.model_dump(by_alias=True))
                
                message = ChatMessage(
                    text="Session timeout",
                    elements=None,
                    user="AI",
                    session_id=session_id,
                    feedback=feedback
                )
                self.tracker["history"].append(message.model_dump(by_alias=True))
                await websocket.send_json(message.model_dump(by_alias=True))
                
                self.tracker["current_node"] = None
            else:
                message = ChatMessage(
                    message_id=None,
                    text=None,
                    elements=None,
                    user="ai_signal",
                    session_id=session_id,
                    feedback=feedback
                )
                self.tracker["history"].append(message.model_dump(by_alias=True))
                await websocket.send_json(message.model_dump(by_alias=True))
                
                timeout_message = self.graph.nodes[current_node]["handler"].timeout
                message = ChatMessage(
                    text=timeout_message,
                    elements=None,
                    user="AI",
                    session_id=session_id,
                    feedback=feedback
                )
                self.tracker["history"].append(message.model_dump(by_alias=True))
                await websocket.send_json(message.model_dump(by_alias=True))
                self.tracker["timeout_iters"] += 1

            
    async def handle_other_node(
        self, 
        websocket: WebSocket,
        keys: List[str], 
        show: bool, 
        element_list: List[Elements], 
        feedback:bool,
        current_node:str,
        ):
        session_id = self.session_id
        current_node = current_node
        text = await self.execute(value=None, keys=keys, current_node=current_node)

        if text and show:

            message = ChatMessage(
                text=text,
                elements=element_list,
                user="AI",
                session_id=session_id,
                feedback=feedback
            ) 
            
            self.tracker["history"].append(message.model_dump(by_alias=True))
            await websocket.send_json(message.model_dump(by_alias=True))
    
    def init(self, timeout, delay):
        self.tracker["current_node"] = self.starter_node
        self.tracker["last_utterance"] = None
        self.tracker["last_response"] = None
        self.tracker["session_id"] = self.session_id
        self.tracker["history"] = []
        self.tracker["timeout_iters"] = 0
        self.tracker["agent_name"] = "Eva" 
        self.tracker["current_intent"] = None
        self.tracker["created_at"] = generate_date_str()
        self.tracker["ended_at"] = None
        self.tracker["name"] = None
        self.tracker["email"] = None
        self.tracker["role"] = None
        self.tracker["data_user_consent"] = False
        self.tracker["application_data"] = {}
        self.tracker["timeout"] = timeout
        self.tracker["delay"] = delay
        self.tracker["origin"] = self.origin

    async def start_flow(self,websocket: WebSocket):
        self.init(240, 0)

        while self.tracker["current_node"] is not None:
            sleep_time = self.tracker["delay"]
            timeout = self.tracker["timeout"]
            current_node = self.tracker["current_node"]
            node_type = self.graph.nodes[current_node]["handler"].type
            keys = self.graph.nodes[current_node]["handler"].saving_keys
            show = self.graph.nodes[current_node]["handler"].show
            elements = self.graph.nodes[current_node]["handler"].elements
            feedback = self.graph.nodes[current_node]["handler"].feedback

            if elements:
                element_list = [Elements(**element) for element in elements]
            else:
                element_list = None

            if node_type == "l":
                await self.handle_listen_node(websocket,keys ,element_list, feedback, current_node, timeout)
            else:
                await self.handle_other_node(websocket, keys, show, element_list, feedback, current_node)

            await aio.sleep(sleep_time)

        message = ChatMessage(
                    message_id=None,
                    text=None,
                    elements=None,
                    user="end_signal",
                    session_id=self.session_id,
                    feedback=feedback
                )
        await websocket.send_json(message.model_dump(by_alias=True))
                
        await websocket.close()

class SessionManager(BaseModel):
    sessions: Dict[str, Session] = {}
    class Config:
        arbitrary_types_allowed = True

    def create_session(self, graph: nx.DiGraph = None, session_id: str = None, origin: str = None):
        session = Session(graph=graph, session_id=session_id, origin=origin)
        
        self.sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Session:
        return self.sessions[session_id]
    
    
    def parse_session_chats(self, chat_history):
        filtered_messages = []
        for message in chat_history:
            if message['user'] in ['USER', 'AI']:
                filtered_messages.append(message)
        return filtered_messages
    
    async def save_messages(self, session_id: str):
        session = self.get_session(session_id)
        chat_history = session.tracker['history']
        filtered_messages = self.parse_session_chats(chat_history)
        message_list = [MessageCreate(**message).model_dump() for message in filtered_messages]
        message_url = f"{settings.chatlog.CHATBOT_CHATLOG_URL}/messages"
        token = settings.chatlog.CHATBOT_CHATLOG_TOKEN
        headers = {"Authorization": f"Bearer {token}"}

        try:
            r = requests.post(
                url=message_url, 
                json=message_list,
                headers=headers
                )
            r.raise_for_status()
        except HTTPException as e:
            logger.error(f"Error saving messages \n {e}")

            
    async def save_session(self, session_id: str):
        session = self.get_session(session_id)
        session.tracker["ended_at"] = generate_date_str()
        session_data = session.tracker
        session_data["session_id"] = session_id
        
        session_dto = SessionCreate(
            created_at=session_data["created_at"],
            ended_at=session_data["ended_at"],
            user_name=session_data["name"],
            user_email=session_data["email"],
            user_role=session_data["role"],
            data_user_consent=session_data["data_user_consent"],
            application_data=session_data["application_data"],
            session_id=session_id,
            metadata=session_data["user_agent"],
            origin=session_data["origin"]
        )
        
        try:
            session_url = f"{settings.chatlog.CHATBOT_CHATLOG_URL}/sessions"
            token = settings.chatlog.CHATBOT_CHATLOG_TOKEN
            headers = {"Authorization": f"Bearer {token}"}
            data = session_dto.model_dump()
            r = requests.post(
                url=session_url, 
                json=data,
                headers=headers
                )
            r.raise_for_status()
        except HTTPException as e:
            logger.error(f"Error saving sessions \n {e}")
     
    async def save(self, session_id: str):
        try:
            await self.save_messages(session_id)
            await self.save_session(session_id)
        except Exception as e:
            logger.error(e)
            
    
    async def delete_session(self, session_id: str):
        del self.sessions[session_id]
        
    async def end_session(self, session_id: str):
        await self.save(session_id)
        await self.delete_session(session_id)
    
    async def get_sessions(self):
        return self.sessions
    
    async def update_session(self, session_id: str, session: Session):
        self.sessions[session_id] = session
        return self.sessions[session_id]
    
    async def get_session_tracker(self, session_id: str):
        return self.sessions[session_id].tracker
    
    async def update_session_from_dict(self, session_id: str, tracker: Dict[str, Any]):
        self.sessions[session_id].tracker = tracker
        return self.sessions[session_id]
    
    async def add_application_data(self, session_id: str, data: Dict[str, Any]):
        self.sessions[session_id].tracker["application_data"] = data
        return self.sessions[session_id]