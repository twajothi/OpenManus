import asyncio
import sys
from pathlib import Path
from app.agent.mvp_manus import MVPManus
from app.logger import logger

async def main():
    """MVP entry point for OpenManus"""
    try:
        agent = MVPManus()
        
        if len(sys.argv) > 1:
            prompt = " ".join(sys.argv[1:])
        else:
            prompt = input("Enter your task: ")
        
        if not prompt.strip():
            logger.warning("Empty prompt provided.")
            return
        
        logger.info("Processing your request...")
        await agent.run(prompt)
        logger.info("Task completed.")
        
    except KeyboardInterrupt:
        logger.warning("Operation interrupted.")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if 'agent' in locals():
            await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
