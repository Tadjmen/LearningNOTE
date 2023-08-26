import os
import time
import threading
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from pyrogram import Client, filters, enums
from datetime import datetime, timedelta
import asyncio

api_id = 'xxx'
api_hash = 'xxx'
app = Client("my_account", api_id=api_id, api_hash=api_hash)
image_folder = "images"
time_limit = timedelta(hours=12)


def telegram_send_image(chatid, photo, caption):
	try:
		app.send_photo(
			chat_id=chatid,
			photo=photo,
			caption=caption
		)
		print("Đã gửi ảnh thành công!")
	except Exception as e:
		print("Đã xảy ra lỗi trong quá trình gửi ảnh:", str(e))

def telegram_send_group_image():
	 app.send_media_group(
		"me",
		[
			InputMediaPhoto("1.jpg"),
			InputMediaPhoto("2.jpg", caption="photo caption")
		]
	)

def telegram_send_text(chatid, text):
	
	try:
		app.send_message(chat_id=chatid, text=text)
		print("Đã gửi văn bản thành công!")
	except Exception as e:
		print("Đã xảy ra lỗi trong quá trình gửi văn bản:", str(e))


def check_time_limit():
	now = datetime.now()
	if now.hour >= 8 and now.hour <= 10:
		return False
	else:
		if os.path.exists("last_image_sent.txt"):
			with open("last_image_sent.txt", "r") as file:
				last_sent_time_str = file.read().strip()
				last_sent_time = datetime.strptime(last_sent_time_str, "%Y-%m-%d %H:%M:%S")
				time_difference = datetime.now() - last_sent_time
				if time_difference <= timedelta(hours=4):
					return False
		return True


def update_last_sent_time():
	current_time = datetime.now()
	with open("last_image_sent.txt", "w") as file:
		file.write(current_time.strftime("%Y-%m-%d %H:%M:%S"))

@app.on_message(filters.photo)
async def my_handler(client, message):
		if message.chat.type in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP, enums.ChatType.CHANNEL]:
				if message.caption is not None and any(keyword in message.caption for keyword in ['Game bài', 'Jackpot', 'Casino', 'Tài Xỉu']):
						return
				#Girls Collection, Girl xinh gái channel
				if message.chat.id in [-1001481234349, -1001669302966, -973243991]:
						if check_time_limit():
								file_path = await client.download_media(message)
								telegram_send_image(-xxx, file_path,"--TeNE--")#NGO
								os.remove(file_path)
								update_last_sent_time()

@app.on_message(filters.group & ~filters.photo)
def on_group_message(client, message):
		if message.text is not None and "@all" == message.text.lower():
				users = client.get_chat_members(message.chat.id)
				usernames = []
				for user in users:
						if user.user.username is not None:
								usernames.append(user.user.username)
						else:
								if user.user.last_name is not None:
										usernames.append(f"[{user.user.first_name} {user.user.last_name}](tg://user?id={user.user.id})")
								else:
										usernames.append(f"[{user.user.first_name}](tg://user?id={user.user.id})")
				if usernames:
						message_text = " ".join(f"@{username}" for username in usernames)
						telegram_send_text(message.chat.id, f"Hi {message_text}, bạn đã được triệu hồi!")


def download_images_from_fb():
	while True:
		try:
			# girlvibes.ba, XM, envysenbou, Học Văn, hanxinhgai12
			#fanpage_ids = ['100057221509188', '100045807769917', '100044555528760', '223851021108590', '100053849592559']
			fanpage_ids = ['223851021108590', '100053849592559']
			access_token = 'xxx'
			image_directory = "images"

			if not os.path.exists(image_directory):
				os.makedirs(image_directory)

			chrome_options = Options()
			chrome_options.add_argument("--headless")
			chrome_options.add_argument("--disable-infobars")
			chrome_options.add_argument("--disable-extensions")
			chrome_options.add_argument("--incognito")
			chrome_options.add_argument("--disable-xss-auditor")
			#chrome_options.add_argument('--disable-blink-features=AutomationControlled')
			driver = webdriver.Chrome(options=chrome_options)

			for fanpage_id in fanpage_ids:
				url = f"https://graph.facebook.com/{fanpage_id}/posts?access_token={access_token}"
				response = requests.get(url)
				data = response.json()
				photo_post_ids = []
				num_of_posts = 2
				for post in data["data"]:
					# type is photo
					if post["type"] == "photo":
						photo_post_ids.append(post["id"])
						if len(photo_post_ids) == num_of_posts:
							if photo_post_ids:
								for photo_post_id in photo_post_ids:
									driver.get(f"https://facebook.com/{photo_post_id}")
									time.sleep(2)
									html = driver.page_source
									soup = BeautifulSoup(html, 'html.parser')
									# Click to Image on post
									a_tags = soup.find_all('a', href=lambda href: href and ("/photos/" in href or "/photo/" in href))
									if a_tags:
										href_lists = [a['href'] for a in a_tags]
										for href in href_lists:
											if href.startswith("/"):
												href = "https://www.facebook.com" + href
											driver.get(href)
											time.sleep(2)
											html = driver.page_source
											soup = BeautifulSoup(html, 'html.parser')
											image_tags = soup.find_all('img', {'src': True, 'data-visualcompletion': True, 'data-ft': False})
											if len(image_tags) == 0:
												image_tags = soup.find_all('img', class_='spotlight', src=True)
											for index, image_tag in enumerate(image_tags):
												image_url = image_tag['src']
												image_name = "{}_{}.jpg".format(photo_post_id, index)				
												image_path = os.path.join(image_directory, image_name)
												time.sleep(2)
												
												response = requests.get(image_url)
												with open(image_path, 'wb') as file:
													file.write(response.content)
												print(f"Tải về ảnh: {image_name}")
									time.sleep(2)

		except Exception as e:
			print(f"Lỗi xảy ra: {str(e)}")
			driver.quit()

		time.sleep(10)  # (10 giây)



def check_and_send_image():
	images_dir = "images"
	sent_images_file = "sent_images.txt"

	if not os.path.exists(images_dir):
		os.makedirs(images_dir)

	if not os.path.exists(sent_images_file):
		with open(sent_images_file, "w") as file:
			pass

	while True:
		image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]

		with open(sent_images_file, "r") as file:
			sent_images = set(file.read().splitlines())

		new_images = [img for img in image_files if img not in sent_images]

		if new_images:
			for image_name in new_images:
				file_path = os.path.join(images_dir, image_name)
				print("New image found:", image_name)
				image_name_trimmed = "_".join(image_name.split("_")[:2])
				telegram_send_image(-xxx, file_path, "https://www.facebook.com/"+image_name_trimmed)
				#telegram_send_image(-xxx, file_path, "https://www.facebook.com/"+image_name_trimmed)
				with open(sent_images_file, "a") as file:
					file.write(image_name + "\n")

		# Wait for 5 seconds before checking again
		time.sleep(60)

#check_and_send_image()
check_images_thread = threading.Thread(target=check_and_send_image)
check_images_thread.daemon = True
check_images_thread.start()

download_images_thread = threading.Thread(target=download_images_from_fb)
download_images_thread.daemon = True
download_images_thread.start()

# Run Pyrogram
app.run()
