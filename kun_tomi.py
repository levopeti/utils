import fbchat
from getpass import getpass
import time
import random

# eg.: "beracom@freemail.hu"
username = "beracom@freemail.hu"

password = getpass()
client = fbchat.Client(username, password)

name = "Tamás Kun"
friends = client.searchForUsers(name)  # return a list of names
friend = friends[0]
print("You will send the message to {}.".format(friend.name))

messages = ["Légyszi mennyél edzésre!",
            "Takarodjál tornázni bzdmg!",
            "Maradj dagadt, leszarom!"]

while True:
    # Tuesday 6:00 or Thursday 19:00 or Friday 16:00 or Sunday 18:00
    if (time.localtime(time.time()).tm_wday == 1 and time.localtime(time.time()).tm_hour == 6) or \
            (time.localtime(time.time()).tm_wday == 3 and time.localtime(time.time()).tm_hour == 19) or \
            (time.localtime(time.time()).tm_wday == 4 and time.localtime(time.time()).tm_hour == 16) or \
            (time.localtime(time.time()).tm_wday == 6 and time.localtime(time.time()).tm_hour == 18):
        if 10 > time.localtime(time.time()).tm_min >= 0:
            message = random.choice(messages)
            msg = fbchat.models.Message(text=message)

            sent = client.send(msg, friend.uid)
            if sent:
                print("Messages sent successfully: {}".format(msg.text))

    time.sleep(60 * 10)
