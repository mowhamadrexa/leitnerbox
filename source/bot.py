import os
import sys
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from random import shuffle
from source.models import MessageLog, User, Leitner_Model, Setting
import _thread as threading
from datetime import datetime


# vars:
bot = telepot.Bot('760874948:AAF9Dn6Z1F8DIMUcVrkEds3obLSVxA6kRt0')
message = ''
chat_id = ''
message_id = ''
query_id = ''
user = None
setting = Setting.objects.filter().order_by('priority')[0]


def error_desc(E):
    print(str(E))
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)


def savelog(user, message, msg):
    new = MessageLog(user=user, message=message, metadata=msg)
    new.save()


def management(user, message, message_id):
    if message.lower() == "/clearuser":
        user.mode = ""
        user.temp_data = ""
        user.queue = ""
        user.levels = ""
        user.save()
        bot.sendMessage(chat_id=user.telegram_id, text="Done", reply_to_message_id=message_id)
    elif message.lower() == "/deluser":
        user.delete()
        bot.sendMessage(chat_id=user.telegram_id, text="Done", reply_to_message_id=message_id)
    elif message.lower() == "/deluserfull":
        Leitner_Model.objects.filter(user=user).delete()
        bot.sendMessage(chat_id=user.telegram_id, text="Done", reply_to_message_id=message_id)
        user.delete()
    elif message.lower() == "/deldata":
        Leitner_Model.objects.filter(user=user).delete()
        bot.sendMessage(chat_id=user.telegram_id, text="Done", reply_to_message_id=message_id)
    elif message.lower().startswith("/settime"):
        try:
            h, m = message.split()[-1].split(':')
            user.time_to_ask = datetime.now().replace(minute=int(m)).replace(hour=int(h)).replace(second=0)
            user.save()
            bot.sendMessage(chat_id=user.telegram_id, text="Done", reply_to_message_id=message_id)
        except Exception as E:
            error_desc(E)
            bot.sendMessage(chat_id=user.telegram_id, text="It must be in this format:\n\n/settime 08:30")
    elif message.lower().startswith("/showboxfull"):
        try:
            box = message.split()[-1]
            q = Leitner_Model.objects.filter(user=user, level=int(box))
            if q.count() != 0:
                text = "\n".join(str(i.q + ": " + i.a) for i in q)
                bot.sendMessage(chat_id=user.telegram_id, text=text, reply_to_message_id=message_id)
            else:
                bot.sendMessage(chat_id=user.telegram_id, text="Empty", reply_to_message_id=message_id)
        except Exception as E:
            error_desc(E)
            bot.sendMessage(chat_id=user.telegram_id, text="It must be in this format:\n\n/showboxfull 2")
    elif message.lower().startswith("/showbox"):
        try:
            box = message.split()[-1]
            q = Leitner_Model.objects.filter(user=user, level=int(box))
            if q.count() != 0:
                text = "\n".join(str(i.q) for i in q)
                bot.sendMessage(chat_id=user.telegram_id, text=text, reply_to_message_id=message_id)
            else:
                bot.sendMessage(chat_id=user.telegram_id, text="Empty", reply_to_message_id=message_id)
        except Exception as E:
            error_desc(E)
            bot.sendMessage(chat_id=user.telegram_id, text="It must be in this format:\n\n/showbox 2")
    elif message.lower() == "/showallfull":
        q = Leitner_Model.objects.filter(user=user)
        text = "\n".join(str(i.q + ": " + i.a) for i in q)
        bot.sendMessage(chat_id=user.telegram_id, text=text)
    elif message.lower() == "/showall":
        q = Leitner_Model.objects.filter(user=user)
        text = "\n".join(str(i.q) for i in q)
        bot.sendMessage(chat_id=user.telegram_id, text=text)
    elif message.lower().startswith("/countbox"):
        try:
            box = message.split()[-1]
            q = Leitner_Model.objects.filter(user=user, level=int(box))
            bot.sendMessage(chat_id=user.telegram_id, text=str(q.count()), reply_to_message_id=message_id)
        except Exception as E:
            error_desc(E)
            bot.sendMessage(chat_id=user.telegram_id, text="It must be in this format:\n\n/countbox 2")
    elif message.lower() == "/countall":
        try:
            box = message.split()[-1]
            q = Leitner_Model.objects.filter(user=user)
            bot.sendMessage(chat_id=user.telegram_id, text=str(q.count()), reply_to_message_id=message_id)
        except Exception as E:
            error_desc(E)
            bot.sendMessage(chat_id=user.telegram_id, text="It must be in this format:\n\n/countall 2")
    else:
        bot.sendChatAction(chat_id=user.telegram_id, action='typing')
        bot.sendMessage(chat_id=user.telegram_id, text=setting.telegram_start_text)


def answer(user, message, message_id):
    if user.mode == "" or user.mode == None:
        if "/" not in message:
            query = Leitner_Model.objects.filter(q__iexact=message)
            if query.count() <= 0:
                bot.sendChatAction(chat_id=user.telegram_id, action='typing')
                bot.sendMessage(chat_id=user.telegram_id, text=setting.enter_answer_text,
                                reply_to_message_id=message_id)
                user.mode = "entering_meaning"
                user.temp_data = message
                user.save()
            else:
                for q in query:
                    bot.sendChatAction(chat_id=user.telegram_id, action='typing')
                    bot.sendMessage(chat_id=user.telegram_id, text="<b>" + q.q + "</b>:\n" + q.a,
                                    parse_mode='html')

        elif message.lower() == '/start':
            bot.sendChatAction(chat_id=user.telegram_id, action='typing')
            bot.sendMessage(chat_id=user.telegram_id, text=setting.telegram_start_text)
        else:
            management(user, message, message_id)
    elif user.mode == "entering_meaning":
        if "/" not in message:
            l = Leitner_Model(user=user, q=user.temp_data, a=message, level=1)
            l.save()
            bot.sendChatAction(chat_id=user.telegram_id, action='typing')
            bot.sendMessage(chat_id=user.telegram_id,
                            text="<b>" + l.q + "</b>" + ":\n" + l.a + "\n\n<code>Added successfully</code>",
                            parse_mode='html')
            user.mode = ""
            user.temp_data = ""
            user.save()
        elif message.lower() == '/start':
            bot.sendChatAction(chat_id=user.telegram_id, action='typing')
            bot.sendMessage(chat_id=user.telegram_id, text=setting.telegram_start_text)
        else:
            management(user, message, message_id)
    else:
        management(user, message, message_id)


def create_user(chat_id):
    new = User.objects.get_or_create(telegram_id=chat_id)
    return new[0]


def handle(msg):
    global message
    global message_id
    global chat_id
    global user

    content_type, chat_type, chat_id = telepot.glance(msg)
    user = create_user(chat_id=chat_id)
    message = msg['text']
    message_id = msg['message_id']
    threading.start_new_thread(savelog, (user, message, msg))
    threading.start_new_thread(answer, (user, message, message_id))


def callback(msg):
    global message
    global message_id
    global chat_id
    global user
    global query_id

    message = msg['data']
    chat_id = msg['from']['id']
    message_id = msg['message']['message_id']
    query_id = msg['id']
    user = create_user(chat_id=chat_id)

    try:
        if message.split('-')[-1] == 'reviewing':
            if user.queue != "" and user.queue != None:
                next_q_id = user.queue.split(',')[0]
                next_q = Leitner_Model.objects.get(id=int(next_q_id))
                bot.answerCallbackQuery(query_id, text="let's go")
                bot.sendChatAction(chat_id=user.telegram_id, action='typing')
                markup = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="I Know", callback_data=next_q_id + '-yes-questioning'),
                     InlineKeyboardButton(text="I Don't Know", callback_data=next_q_id + '-no-questioning')],
                ])
                bot.sendMessage(chat_id=user.telegram_id,
                                text='<a href="https://dictionary.cambridge.org/dictionary/english/{0}">'.format(
                                    next_q.q) + next_q.q + "</a>",
                                reply_markup=markup,
                                parse_mode='html',
                                disable_web_page_preview=True)
            else:
                bot.answerCallbackQuery(query_id, text="Well done, That was it for today.")
                user.queue = ""
                user.mode = ""
                user.save()

        elif message.split('-')[-1] == "questioning":
            level_up = True if message.split('-')[1] == 'yes' else False
            q_id = message.split('-')[0]
            q = Leitner_Model.objects.get(id=q_id)

            try:
                if q.level + 1 <= 5 and level_up:
                    q.level += 1
                    print(1)
                elif q.level - 1 >= 1 and not level_up:
                    q.level -= 1

            except Exception as E:
                print(str(E))

            q.save()
            good = ['Perfecto', 'Fantastic', 'I knew you can', 'YES', 'That\'s my boy', 'There you go', 'The legend',
                    'Hats off to you']
            bad = ['You Stink', 'Wrong', 'COmmooon', 'What the hell man', 'What the hell', 'Shit', 'heh', 'got ya']
            shuffle(good)
            shuffle(bad)
            bot.answerCallbackQuery(query_id, text=(good[0] if level_up else bad[0]) + '- Box ' + str(q.level))

            queue = user.queue.split(',')
            del queue[0]
            user.queue = (','.join(str(i) for i in queue))
            user.save()

            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Next", callback_data=user.telegram_id + '-reviewing')],
            ])
            bot.sendMessage(chat_id=user.telegram_id,
                            text='<a href="https://dictionary.cambridge.org/dictionary/english/{0}">'.format(
                                q.q) + q.q + '</a>:\n\n' + q.a,
                            parse_mode='html',
                            disable_web_page_preview=True,
                            reply_markup=markup)

    except Exception as E:
        print(str(E))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        bot.sendMessage(chat_id=user.telegram_id, text='An error occured, Please try later.')


def main():
    global bot
    bot.message_loop({'chat': handle, 'callback_query': callback, 'inline_query': callback},timeout=100)
    print('Connected to Telegram...')


if __name__ == '__main__':
    main()
