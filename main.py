import asyncio
from telethon import TelegramClient, events, sync
import re

from config import REGEX_PATTERNS_COMMON, REGEX_PATTERNS_CRITICAL
from bark import bark

# ------------------- 配置信息 -------------------
# 将下面的 "YOUR_API_ID" 和 "YOUR_API_HASH" 替换为您自己的值
API_ID = 123456
API_HASH = "xxxxxxx"

# 为您的会话起一个名字
SESSION_NAME = "my_telegram_session"

# ------------------- 目标频道 -------------------
# 在此处填入您想监听的频道的用户名或聊天 ID
# 如果是公开频道，可以使用其用户名，例如: "PyrogramChat"
# 如果是私有频道或希望使用 ID，请填入其聊天 ID，例如: -1001695180959
TARGET_CHANNEL = -1001695180959  # 或者 -1001695180959

# 创建 Telethon 客户端实例
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# 连接到 Telegram
async def main():
    await client.start()

    # 监听所有公共频道的消息
    # @client.on(events.NewMessage)

    # 获取频道的实体信息
    channel = await client.get_entity(TARGET_CHANNEL)

    # 监听该频道的新消息
    @client.on(events.NewMessage(chats=channel))
    async def handler(event):
        # print(f"新消息: {event.message}")

        content = event.text
        title = content.split("](")[0][3:].strip("*")
        url = content.split("](")[1][:-1]
        print(f"Title: {title}, URL: {url}")

        # 遍历所有正则表达式
        for pattern in REGEX_PATTERNS_CRITICAL:
            if re.search(pattern, title, re.IGNORECASE):
                bark(title, url, True, True)
                break

        for pattern in REGEX_PATTERNS_COMMON:
            if re.search(pattern, title, re.IGNORECASE):
                bark(title, url, True, False)
                break

    # 持续监听消息
    await client.run_until_disconnected()

# 启动客户端
client.loop.run_until_complete(main())