from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import asyncio
from dotenv import load_dotenv
import os

from tv_interval_utils import normalize_interval
from json_parse import parse_tv_payload

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID_STR = os.getenv("TELEGRAM_CHAT_ID")
TOPIC_ID_STR = os.getenv("TELEGRAM_TOPIC_ID")

if not BOT_TOKEN or not CHAT_ID_STR or not TOPIC_ID_STR:
    raise ValueError("Missing env variables")

CHAT_ID = int(CHAT_ID_STR)
TOPIC_ID = int(TOPIC_ID_STR)
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

app = FastAPI()
msg_queue = asyncio.Queue()

# Telegram 消息发送器（节流 + 异步队列）
async def telegram_worker():
    while True:
        msg = await msg_queue.get()
        try:
            payload = {
                "chat_id": CHAT_ID,
                "message_thread_id": TOPIC_ID,
                "text": msg
            }
            async with httpx.AsyncClient() as client:
                resp = await client.post(TELEGRAM_API, json=payload)
                print("Telegram response:", resp.status_code, resp.text)
        except Exception as e:
            print("发送 Telegram 消息失败:", e)
        await asyncio.sleep(1.5)  # Telegram 流控限制：约每秒最多1条

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(telegram_worker())

@app.post("/webhook/tradingview")
async def tradingview_webhook(req: Request):
    try:
        body = await req.body()
        body_text = body.decode("utf-8", errors="replace")
        print("Webhook JSON 内容:", body_text)

        msg = parse_tv_payload(body_text)
        await msg_queue.put(msg)
        return JSONResponse(content={"status": "queued"})

    except Exception as e:
        print("解析异常:", e)
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
