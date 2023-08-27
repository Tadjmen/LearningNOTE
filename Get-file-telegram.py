from pyrogram import Client
import asyncio

async def main():
	api_id = xxx  # 1688
	api_hash = 'xxx'
	chatid = '-xxx'

	async with Client("my_account", api_id, api_hash) as app:
		chat = await app.get_chat(chatid)  

		while True:
			async for message in app.search_messages(chat_id=chatid):
				if message.media and message.document:
					try:
						with open('downloaded.txt', 'r') as f:
							downloaded_files = f.read().splitlines()
						
						if ((str(message.chat.id) + "_" + str(message.id))) not in downloaded_files:
							if message.media_group_id is None:
								async def progress(current, total):
									print(f"{current * 100 / total:.1f}%")
								await app.download_media(message, progress=progress)
								print(f"Đã tải xuống: {message.document.file_name}")
								with open('downloaded.txt', 'a') as f:
									f.write(str(message.chat.id) + "_" + str(message.id) + '\n')
							else:
								await app.download_media(message.document.file_id, file_name=message.document.file_name)
								print(f"Đã tải xuống: {message.document.file_name}")
								with open('downloaded.txt', 'a') as f:
									f.write(str(message.chat.id) + "_" + str(message.id) + '\n')
					except AttributeError:
						print("Tin nhắn không chứa đính kèm document")

			await asyncio.sleep(10)

if __name__ == "__main__":
	asyncio.run(main())
