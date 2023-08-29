from pyrogram import Client
import os

# Thay thế bằng thông tin tài khoản của bạn
api_id = xxx                                           #1688
api_hash = 'xxx'

with Client("my_account", api_id=api_id, api_hash=api_hash) as app:
    dialogs = app.get_dialogs()

    for dialog in dialogs:
        chat_id = dialog.chat.id
        chat_title = dialog.chat.title
        print("Chat ID:", chat_id, "Chat Title:", chat_title)
