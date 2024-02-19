import time
import telepot
from telepot.loop import MessageLoop

bot_token = '6697142766:AAH31EaTn5wHo7f96ilQ3xj_EYAatBl3k14'

CHAT_ID = '1189260508'
ALLOWED_CHAT_IDS = ['1189260508']

bot = telepot.Bot(bot_token)

bot_request_delay = 0.5
last_time_bot_ran = 0

user_chat_id = ''
is_adding_chat_id = False
is_removing_chat_id = False

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_photo(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': "Hello",
        'parents': [PARENT_FOLDER_ID]
    }

    media = MediaFileUpload(file_path)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

def handle_new_messages(msg):
    global user_chat_id, is_adding_chat_id, is_removing_chat_id

    chat_id = msg['chat']['id']
    text = msg['text']
    from_name = msg['from']['first_name']

    print(f"Received message '{text}' from user {chat_id}")

    if str(chat_id) not in ALLOWED_CHAT_IDS:
        bot.sendMessage(chat_id, "Unauthorized user")
        return

    if text == '/start':
        welcome = f"Welcome, {from_name}.\n"
        welcome += "Use the following commands to control the system:\n\n"
        welcome += "/A - Live Feed\n"
        welcome += "/B - Cradle Swing Control\n"
        welcome += "/C - Lullaby Control\n"
        welcome += "/Users - Check Allowed Chat IDs\n"
        welcome += "/User_add - Add Chat ID\n"
        welcome += "/User_remove - Remove Chat ID\n"
        bot.sendMessage(chat_id, welcome)
    elif text == '/A':
        pass
    elif text == '/C':
        lullaby = f"/1 - Play Lullaby\n"
        lullaby += "/2 - Edit Song List\n"
        bot.sendMessage(chat_id, lullaby)
    elif text == '/2':
        bot.sendMessage(chat_id, "https://drive.google.com/drive/u/1/folders/1JqubTwwfcgv3sANDKn6dROQaf8uGXzXy")
    elif text == '/3':
        bot.sendMessage(chat_id, ngrok_tunnel.public_url)
    elif text == '/Users':
        message = "Allowed Chat IDs:\n" + '\n'.join(ALLOWED_CHAT_IDS)
        bot.sendMessage(chat_id, message)
    elif text == '/User_add':
        if str(chat_id) == CHAT_ID:
            bot.sendMessage(chat_id, "Please provide the chat ID you want to add to the allowed list:")
            is_adding_chat_id = True
        else:
            bot.sendMessage(chat_id, "Unauthorized access. Only the bot owner can grant user control.")
    elif is_adding_chat_id and str(chat_id) == CHAT_ID:
        if not user_chat_id:
            user_chat_id = text
            bot.sendMessage(chat_id, "Please enter the chat ID again to confirm:")
        elif user_chat_id == text:
            ALLOWED_CHAT_IDS.append(user_chat_id)
            bot.sendMessage(chat_id, "User chat ID added to allowed list.")
            user_chat_id = ''
            is_adding_chat_id = False
    elif text == '/User_remove':
        if str(chat_id) == CHAT_ID:
            bot.sendMessage(chat_id, "Please provide the chat ID you want to remove from the allowed list:")
            is_removing_chat_id = True
        else:
            bot.sendMessage(chat_id, "Unauthorized access. Only the bot owner can remove users.")
    elif is_removing_chat_id and str(chat_id) == CHAT_ID:
        if text in ALLOWED_CHAT_IDS:
            ALLOWED_CHAT_IDS.remove(text)
            bot.sendMessage(chat_id, "User chat ID removed from allowed list.")
        else:
            bot.sendMessage(chat_id, "The provided chat ID was not found in the allowed list.")
        is_removing_chat_id = False
    else:
        bot.sendMessage(chat_id, "Invalid Input")
        welcome = f"Welcome, {from_name}.\n"
        welcome += "Use the following commands to control the system:\n"
        welcome += "/A - Live Feed\n"
        welcome += "/B - Cradle Swing\n"
        welcome += "/C - Start Lullaby\n"
        welcome += "/Users - Check Allowed Chat IDs\n"
        welcome += "/User_add - Add Chat ID\n"
        welcome += "/User_remove - Remove Chat ID\n"
        bot.sendMessage(chat_id, welcome)

def on_chat_message(msg):
    global last_time_bot_ran
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        handle_new_messages(msg)

MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()
print("Telegram Bot Started...")

while True:
    time.sleep(bot_request_delay)