import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock
from llm_client import LLMClient

@pytest.fixture
def llm_client():
    return LLMClient()

@pytest.fixture
def llm_client_with_prompt():
    # Create a temporary system prompt file
    temp_prompt = Path("temp_system_prompt.txt")
    temp_prompt.write_text("You are a helpful assistant.")
    client = LLMClient(system_prompt_path=temp_prompt)
    yield client
    # Cleanup
    temp_prompt.unlink()

@pytest.mark.asyncio
async def test_initialization():
    client = LLMClient()
    assert client.base_url == "http://127.0.0.1:1234"
    assert client.headers == {"Content-Type": "application/json"}
    assert client.system_prompt == ""

@pytest.mark.asyncio
async def test_initialization_with_system_prompt(llm_client_with_prompt):
    assert llm_client_with_prompt.system_prompt == "You are a helpful assistant."

@pytest.mark.asyncio
async def test_generate_response_success():
    client = LLMClient()
    mock_response = {
        "choices": [
            {
                "message": {
                    "content": "Test response"
                }
            }
        ]
    }
    
    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_context = MagicMock()
        mock_context.status = 200
        async def mock_json():
            return mock_response
        mock_context.json = mock_json
        mock_post.return_value.__aenter__.return_value = mock_context
        
        response = await client.generate_response("Test message")
        assert response == "Test response"

@pytest.mark.asyncio
async def test_generate_response_api_error():
    client = LLMClient()
    
    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_context = MagicMock()
        mock_context.status = 500
        async def mock_text():
            return "Internal Server Error"
        mock_context.text = mock_text
        mock_post.return_value.__aenter__.return_value = mock_context
        
        response = await client.generate_response("Test message")
        assert isinstance(response, dict)
        assert "error" in response

@pytest.mark.asyncio
async def test_test_connection_success():
    client = LLMClient()
    
    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_context = MagicMock()
        mock_context.status = 200
        async def mock_json():
            return {"choices": [{"message": {"content": "Test"}}]}
        mock_context.json = mock_json
        mock_post.return_value.__aenter__.return_value = mock_context
        
        is_connected = await client.test_connection()
        assert is_connected is True

@pytest.mark.asyncio
async def test_test_connection_failure():
    client = LLMClient()
    
    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_post.return_value.__aenter__.return_value.status = 500
        
        is_connected = await client.test_connection()
        assert is_connected is False 