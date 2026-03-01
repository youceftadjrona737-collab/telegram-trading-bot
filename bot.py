import os
import requests
import pandas as pd
import ta
import time
from datetime import datetime
from telegram import Bot

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = Bot(token=TOKEN)

def get_data():
    url = "https://api.binance.com/api/v3/klines?symbol=EURUSDT&interval=5m&limit=150"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df[4] = df[4].astype(float)
    return df

def analyze():
    df = get_data()
    df["ema9"] = ta.trend.EMAIndicator(df[4], window=9).ema_indicator()
    df["ema21"] = ta.trend.EMAIndicator(df[4], window=21).ema_indicator()
    df["rsi"] = ta.momentum.RSIIndicator(df[4], window=14).rsi()
    
    last = df.iloc[-1]
    
    if last["ema9"] > last["ema21"] and last["rsi"] > 50:
        return "BUY"
    elif last["ema9"] < last["ema21"] and last["rsi"] < 50:
        return "SELL"
    else:
        return None

def send_signal(signal):
    now = datetime.now().strftime("%H:%M")
    message = f"""
🔥 QUOTEX SIGNAL 🔥

⏰ Time: {now}
⌛ Expiry: 5 Minutes
📊 Pair: EUR/USD
📈 Type: {signal}
"""
    bot.send_message(chat_id=CHAT_ID, text=message)

while True:
    signal = analyze()
    if signal:
        send_signal(signal)
    time.sleep(300)
