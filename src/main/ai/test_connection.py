import asyncio
import logging
from llm_client import LLMClient

logging.basicConfig(level=logging.INFO)

async def main():
    client = LLMClient()
    
    # Test connection
    logging.info("Testing connection to LM Studio...")
    is_connected = await client.test_connection()
    logging.info(f"Connection test result: {'Success' if is_connected else 'Failed'}")
    
    if is_connected:
        # Test message generation
        test_message = "What is 2+2? Please answer with just the number."
        logging.info(f"Sending test message: {test_message}")
        response = await client.generate_response(
            test_message,
            temperature=0.1,  # Low temperature for more deterministic response
            max_tokens=10     # Small response size for testing
        )
        logging.info(f"Response received: {response}")

if __name__ == "__main__":
    asyncio.run(main()) 