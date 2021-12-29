"""
App api_id: 17086774
App api_hash: f0a5b0c177906f6f145698c704f0d345
App title: jobs_dashboard
Short name: jobsdashboard2021

"""

# import nest_asyncio
import asyncio

# nest_asyncio.apply()


from telethon import TelegramClient, client
from telethon.sessions import StringSession
from telethon.tl.types import User
from telethon.tl.types.auth import SentCode
from telethon.errors import SessionPasswordNeededError

import os
from dotenv import load_dotenv

load_dotenv()

# Use your own values from my.telegram.org
api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
phone_number = os.getenv("phone_number")

states_messages = {
    "auth_succeeded": "Great, Welcome again {user_name}!",
    "auth_failed": "Oops, Telegram login failed, try again after a while.",
    "code_requested": "We sent code to your telegram account, please write it down.",
    "password_required": "Your account has 2FA and needs your password to login.",
}


async def auth(
    phone_number: str,
    user_session_string: str or None = None,
    code: str or None = None,
    password: str or None = None,
    phone_code_hash: str or None = None,
):
    state: dict
    user: User or SentCode or None = None
    print(user_session_string)
    client = TelegramClient(StringSession(user_session_string), api_id, api_hash)
    await client.connect()

    if await client.is_user_authorized():
        user = await client.get_me()

        state = {"code": "auth_succeeded", "message": states_messages["auth_succeeded"]}
        # return state, user, client
        return state, user
    print({"code_before_if": code})
    if not code:
        # await client.send_code_request(phone_number)
        phone_code_hash = await client.send_code_request(phone_number)
        state = {
            "code": "code_requested",
            "message": states_messages["code_requested"],
            "phone_code_hash": phone_code_hash,
        }
        # return state, user

    try:
        # user = await client.sign_in(
        #     phone=phone_number, code=code or input("Enter code: ")
        # )
        print({"code": code, "phone_code_hash": phone_code_hash})
        user = await client.sign_in(
            phone=phone_number, code=code or input("Enter code: ")
        )
        # user = await client.sign_in(
        #     phone=phone_number, code=code ,phone_code_hash=phone_code_hash
        # )
    except SessionPasswordNeededError:
        user = await client.sign_in(password=password or input("Enter password: "))
        # print({"password": password})
        # if not password:
        # state = {
        # "code": "password_required",
        # "message": states_messages["password_required"],
        # }
        # return state, user, client
        # return state, user

        # user = await client.sign_in(password=password)

    user_session_string = client.session.save()
    # print("User session string: " + user_session_string)

    state = {
        "code": "auth_succeeded",
        "message": states_messages["auth_succeeded"],
        "user_session_string": user_session_string,
    }
    # return state, user, client
    return state, user


async def main(user: User or SentCode, client: TelegramClient):
    # Getting information about yourself

    # "user" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    # print(user.stringify())
    # print(client.session.save())
    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = user.username
    print(username)
    print(user.phone)

    # You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, "has ID", dialog.id)

    # You can send messages to yourself...
    await client.send_message("me", "Hello, myself!")
    # ...to some chat ID
    # await client.send_message(-100123456, "Hello, group!")
    # ...to your contacts
    # await client.send_message("+34600123123", "Hello, friend!")
    # ...or even to any username
    # await client.send_message("username", "Testing Telethon!")

    # You can, of course, use markdown in your messages:
    message = await client.send_message(
        "me",
        "This message has **bold**, `code`, __italics__ and "
        "a [nice website](https://example.com)!",
        link_preview=False,
    )

    # Sending a message returns the sent message object, which you can use
    print(message.raw_text)

    # You can reply to messages directly if you have a message object
    await message.reply("Cool!")

    # Or send files, songs, documents, albums...
    # await client.send_file("me", "./E2vsrCfVoAIWC9L.png")

    # You can print the message history of any chat:
    # async for message in client.iter_messages("Front End Vacancies"):
    #     print(message.stringify())
    #     break

    # You can download media from messages, too!
    # The method will return the path where the file was saved.
    # if message.photo:
    # path = await message.download_media()
    # print("File saved to", path)  # printed after download is done


# with client:


def init(
    phone_number: str,
    code: str or None = None,
    password: str or None = None,
    phone_code_hash: str or None = None,
    user_session_string: str or None = None,
):
    print(user_session_string)
    # user, client = asyncio.get_event_loop().run_until_complete(auth(phone_number,code=code,password=password))
    state, user = asyncio.get_event_loop().run_until_complete(
        auth(
            phone_number=phone_number,
            user_session_string=user_session_string,
            password=password,
            code=code,
            phone_code_hash=phone_code_hash,
        )
    )
    # print(user)
    # asyncio.get_event_loop().run_until_complete(main(user, client))
    # print(user)
    return {"state": state}
