from fastapi import FastAPI
from bot import setup_bot
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    global bot_application
    bot_application = await setup_bot()

@app.on_event("shutdown")
async def on_shutdown():
    await bot_application.stop()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
