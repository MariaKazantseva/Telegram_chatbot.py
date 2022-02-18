from pyrogram import Client, filters, emoji
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup


@Client.on_message(filters.command(["start"]))
def bot_start(_, message):
    message.reply(
        "Hello! This is Sra. Masha's replica speaking. First of all, are you in a good mood to talk to  Sra. Masha?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Yes, I am! I will be respectful" + " " + emoji.SMILING_FACE_WITH_SMILING_EYES,
                                         callback_data="yes_1")
                ],
                [
                    InlineKeyboardButton("Hmm, I need some preparation" + " " + emoji.THINKING_FACE,
                                         callback_data="no_1"),
                ],
            ]
        )
    )


def filter_query_1(_, __, query):
    return query.data == "yes_1" or query.data == "no_1"


@Client.on_callback_query(filters.create(filter_query_1))
def flow_answer_1(_, callback_query):
    question_2(callback_query.message) if callback_query.data == "yes_1" else question_2_end(callback_query.message)


def question_2_end(message):
    message.reply(f"Get prepared and come back later then. Bye! {emoji.COW}")


def question_2(message):
    message.reply(
        "Ok, let's get down to business, Masha here. Why have you decided to contact me?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"I have a personal message {emoji.DIZZY}", callback_data="personal")
                ],
                [
                    InlineKeyboardButton(f"Other type of information  {emoji.INFORMATION}", callback_data="other")
                ],
            ]
        )
    )


def filter_query_2(_, __, query):
    return query.data == "personal" or query.data == "other"


@Client.on_callback_query(filters.create(filter_query_2))
def flow_answer_2(_, callback_query):
    question_3_personal(callback_query.message) if callback_query.data == "personal" else question_3_other(
        callback_query.message)


def question_3_personal(message):
    message.reply(
        "What kind of message?",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["Urgent", "Not urgent",
                 " Not urgent at all!"],
            ],
            resize_keyboard=True, one_time_keyboard=True
        )
    )


def question_3_other(message):
    message.reply(
        "What kind of information would you like to ask?",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["It is related to work. ", "It is an ad or a promotion"],
            ],
            resize_keyboard=True, one_time_keyboard=True
        )
    )


@Client.on_message(filters.text | filters.voice)
def messy_client(client, message):
    global message_allowed
    my_list = [
                ["Urgent", "Better call me then!" + emoji.CALL_ME_HAND, False],
                ["Not urgent", "Go ahead and type it!" + emoji.WRITING_HAND, True],
                ["Not urgent at all!", "Go ahead, type it or record it!", True],
                ["It is related to work.", "Please, send it to: https://www.linkedin.com/in/masha-kazantseva-452603125/", False],
                ["It is an ad or a promotion", "Please, do not disturb me. I have everything I need.", False]
            ]
    for i in my_list:
        if i[0] == message.text:
            message.reply(i[1])
            message_allowed = i[2]
            return 0
    if not message_allowed:
        message.reply(emoji.POUTING_FACE + "Follow the rules!")
        message.reply("/start")
    else:
        from_contact = f"{message.chat.username} ({message.chat.first_name} {message.chat.last_name})"
        client.send_message(chat_id="eres_un_sol", text=from_contact)
        if message.text is not None:
            client.send_message(chat_id="eres_un_sol", text=message.text)
        if message.voice is not None:
            client.send_voice(chat_id="eres_un_sol", voice=message.voice.file_id)
        message.reply("Thanks! I will answer soon")


message_allowed = False
