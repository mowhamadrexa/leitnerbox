from django.shortcuts import render
from source.bot import main
from _thread import start_new_thread
from time import sleep
from datetime import datetime
from source.models import User, Leitner_Model
from source.bot import bot
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup


# Create your views here.
def test():
    while True:
        users = User.objects.all()
        for user in users:
            if user.mode == "reviewing":
                continue
            levels = [1]
            datas = Leitner_Model.objects.filter(user=user).order_by('date_of_create')
            try:
                first_date = datas[0].date_of_create
            except:
                continue
            now = datetime.now()
            delta = now - first_date

            if delta.days != 0:
                if delta.days % 2 == 0:
                    levels.append(2)
                if delta.days % 7 == 0:
                    levels.append(3)
                if delta.days % 14 == 0:
                    levels.append(4)
                if delta.days % 30 == 0:
                    levels.append(5)

            user.levels = (','.join(str(i) for i in levels))

            if user.queue == "" or user.queue == None:
                queue = Leitner_Model.objects.filter(level__in=levels, user=user).order_by('level')
                user.queue = (','.join(str(q.id) for q in queue))

            user.save()

            if (
                    user.queue != "" and user.queue != None and user.time_to_ask.hour == now.hour and user.time_to_ask.minute == now.minute):
                user.mode = "reviewing"
                markup = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Let's do this", callback_data=user.telegram_id + '-reviewing')],
                ])
                bot.sendMessage(chat_id=user.telegram_id, text="It's time to review", parse_mode='html',
                                reply_markup=markup)
            user.save()

        sleep(60)


start_new_thread(main, ())
start_new_thread(test, ())
