
# https://www.pythonanywhere.com/user/imvickykumar999/tasks_tab/
import requests

bot_token = '6297291074:AAFzpuG7i3GNqUgx9Wj5JNxHF6WF_TCufhk'
gets = f'https://api.telegram.org/bot{bot_token}/getUpdates'
req = requests.get(gets) 

show = req.json()
lst = list(show.values())[1]
fetch = lst[-1]['message']['text']

bot_message = 'Welcome, this message is sent automatically.'
bot_chatID = lst[-1]['message']['chat']['id']

sets = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'    
x = requests.post(sets)
print(x.text)
