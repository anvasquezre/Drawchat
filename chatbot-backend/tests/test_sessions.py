# test_session.py

import pytest
from unittest.mock import patch, MagicMock

from v1.src.session import Session, SessionManager

@pytest.mark.asyncio
async def test_session_init():
    session = Session()
    assert session.session_id is not None
    assert session.tracker["current_node"] == Session.starter_node

@pytest.mark.asyncio
async def test_handle_listen_node(mocker):
    mock_websocket = MagicMock()
    mock_chatmessage = mocker.patch("session.ChatMessage")
    
    session = Session()
    await session.handle_listen_node(mock_websocket, ["last_utterance"], [], True, "node1", 120)
    
    calls = [
        mocker.call(user="listen_signal"),
        mocker.call(user="USER"),
        mocker.call(user="ai_signal")
    ]
    mock_chatmessage.assert_has_calls(calls)
    
    mock_websocket.send_json.assert_awaited()
    mock_websocket.receive_json.assert_awaited()
    
@pytest.mark.asyncio    
async def test_handle_other_node(mocker):
    mock_websocket = MagicMock()
    mock_chatmessage = mocker.patch("session.ChatMessage")
    
    session = Session()
    await session.handle_other_node(mock_websocket, ["last_response"], True, [], False, "node2")

    mock_chatmessage.assert_called_once_with(user="AI")
    mock_websocket.send_json.assert_awaited()

@pytest.mark.asyncio
async def test_start_flow(mocker):
    mock_websocket = MagicMock()
    mock_chatmessage = mocker.patch("session.ChatMessage")
    graph = mocker.AsyncMock()
    
    session = Session(graph=graph)
    await session.start_flow(mock_websocket)
    
    graph.assert_awaited()
    assert session.tracker["current_node"] is None
    mock_chatmessage.assert_called_with(user="end_signal")
    mock_websocket.close.assert_awaited()
    
@pytest.mark.asyncio
async def test_session_manager_create(mocker):
    manager = SessionManager()
    session = manager.create_session()
    assert len(manager.sessions) == 1
    assert session.session_id in manager.sessions
    
@pytest.mark.asyncio    
async def test_session_manager_get(mocker):
    manager = SessionManager()
    session = manager.create_session()
    retrieved = await manager.get_session(session.session_id)
    assert retrieved.session_id == session.session_id