import logging
import uvicorn
from threading import Thread
from bot.main import start_bot
from tasks.scheduler import start_scheduler
from api.main import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def main():
    logger.info("🚀 Starting the bot, API, and background tasks...")

    api_thread = Thread(target=run_api, daemon=True)
    api_thread.start()

    start_scheduler()

    start_bot()

if __name__ == "__main__":
    main()