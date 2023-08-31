from pyrogram import Client
import asyncio
import datetime
import os

async def main():
	api_id = xxx  # 1688
	api_hash = 'xxx'
	chatid = '-xxx'

	start_time = '2023-04-29 00:00:00'
	end_time = '2023-08-29 00:00:00'

	start_time_dt = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
	end_time_dt = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
	async with Client("my_account", api_id, api_hash) as app:
		chat = await app.get_chat(chatid)  

		while True:
			async for message in app.search_messages(chat_id=chatid):
				if message.media and message.document:
					try:
						message_time = message.document.date
						if start_time_dt <= message_time <= end_time_dt:
							with open('downloaded.txt', 'r') as f:
								downloaded_files = f.read().splitlines()
							
							if ((str(message.chat.id) + "_" + str(message.id))) not in downloaded_files:
								if message.media_group_id is None:
									async def progress(current, total):
										print(f"{current * 100 / total:.1f}%")
									await app.download_media(message, progress=progress)
									current_time = datetime.datetime.now()
									file_stats = os.stat('downloads/' + message.document.file_name)
									print(f"Đã tải xuống: {message.document.file_name} at {current_time}")
									if file_stats.st_size > 1024:
										with open('downloaded.txt', 'a') as f:
											f.write(str(message.chat.id) + "_" + str(message.id) + '\n')
								else:
									await app.download_media(message.document.file_id, file_name=message.document.file_name)
									current_time = datetime.datetime.now()
									file_stats = os.stat('downloads/' + message.document.file_name)
									print(f"Đã tải xuống: {message.document.file_name} at {current_time}")
									if file_stats.st_size > 1024:
										with open('downloaded.txt', 'a') as f:
											f.write(str(message.chat.id) + "_" + str(message.id) + '\n')
					except Exception as e:
						print("An error occurred:", e)

			await asyncio.sleep(10)

if __name__ == "__main__":
	asyncio.run(main())
