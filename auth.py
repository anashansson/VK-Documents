# -*- coding: utf-8 -*-
import codecs
import requests
import urllib
import webbrowser
import json
import os
import math
import time
import logger

# Настройки приложения
client_id = "3998121"
client_secret = "AlVXZFMUqyrnABp8ncuU"

# Функция обращения к API
def api_call(method, param):
	api_url = "https://api.vk.com/method/" + method + "?" + urllib.urlencode(param)
	s = requests.Session()
	r = s.get(api_url)

	response = json.loads(r.text)

	if(len(response["response"]) > 0):
		return response["response"][0]
	else:
		return response["response"]

# Вычисляем размер файла
def size(size_bytes):
	if (size_bytes == 0):
		return '0 B'
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes/p, 2)
	return '%s %s' % (s, size_name[i])

# Вывод простых ошибок
def error():
	logger.fail("Пусто!")

# Если нет папки для документов создаем
if not os.path.exists("./docs/"):
	os.makedirs("./docs/")

# Проверяем есть ли файл с access_token
if os.path.isfile("./access_token.txt"):
	file = open("./access_token.txt", "r")
	access_token = file.read()
	file.close()

	logger.success("Авторизовались!")
else:
	data = {
		"client_id": client_id,
		"redirect_uri": "https://oauth.vk.com/blank.html",
		"display": "page",
		"scope": "docs,offline",
		"response_type": "token",
		"v": "5.0"
	}

	url = "https://oauth.vk.com/authorize?" + urllib.urlencode(data)

	webbrowser.open(url, new=2)

	logger.info("В браузере нужно разрешить приложение получение access_token");
	logger.info("После этого скопируйте значение параметра access_token из браузерной строки")

	access_token = raw_input("[~] Введите параметр access_token из браузера: ")

	if len(access_token) > 0:
		logger.success("Авторизовались!")

		file = open("./access_token.txt", "w")
		file.write(access_token)
		file.close()
	else:
		error()

# Ищем документы
user_id = raw_input("[~] Введите ID пользователя: ")

if len(user_id) > 0:
	user_id = user_id.replace("id","")

	start_from = raw_input("[~] Введите число в диапазоне от 0 до 999999999: ")

	if len(start_from) > 0:
		while int(start_from) < 999999999:
			result = api_call("docs.getById", {
				"docs": str(user_id) + "_" + str(start_from),
				"access_token": access_token
			})

			try:
				if os.path.isfile("./docs/" + str(user_id) + "_" + str(start_from) + "." + str(result["ext"])):
					logger.success("Повтор файла: " + str(user_id) + "_" + str(start_from) + "." + str(result["ext"]) + " [" + size(result["size"]) +  "]")
				else:
					logger.success("Скачиваем файл: " + str(user_id) + "_" + str(start_from) + "." + str(result["ext"]) + " [" + size(result["size"]) +  "]")
					urllib.urlretrieve(result["url"], "./docs/" + str(user_id) + "_" + str(start_from) + "." + str(result["ext"]))
			except: 
				logger.warning(str(user_id) + "_" + str(start_from) + ": пустой!")

			start_from = int(start_from) + 1
			time.sleep(.5)
	else:
		error()
else:
	error()


