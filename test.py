import requests

url = "https://api.telegram.org/bot8251195978:AAEfr5-Bs9hDhl-8_SUuqm4X5nMfe8KBpSg/sendMessage"
payload = {
    "chat_id": -1002831756914,
    "message_thread_id": 1325,
    "text": "测试消息"
}

response = requests.post(url, json=payload)
print(response.status_code, response.text)
