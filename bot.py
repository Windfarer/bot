import random
import wxpy
import re

dice_pattern = re.compile(r'''([+-]{0,1}(\d+)[Dd](\d+))|([+-]{0,1}(\d+))''')

def roll(text, limit=1000):
    groups = dice_pattern.findall(text)
    result = []
    for group in groups:
        sub_result = []
        if group[0]:
            if group[0].startswith('-'):
                sign = -1
            else:
                sign = 1
            for _ in range(int(group[1])):
                n = int(group[2])
                if n > limit:
                    return []
                sub_result.append(sign * random.randint(1, n))
        elif group[3]:
            sub_result.append(int(group[3]))
    return result


bot = wxpy.Bot(console_qr=True, cache_path='/data/wxpy.pkl')

group = bot.groups()

HELP_TEXT = "使用说明:\n" \
            ".r 骰子个数d面数，\n" \
           "如「 .r 2d6 」即为掷2个6面的骰子"

def help(msg):
    return HELP_TEXT

def roll_dice(msg):
    if msg.type == wxpy.TEXT and msg.text.startswith(".r"):
        sender = msg.member.name if msg.member else msg.sender.name
        text = msg.text[2:].strip()
        try:
            result = roll(text.split(" ", 2)[0])
            if result:
                print(result)
                return "{} 掷了骰子「 {} 」\n" \
                       "掷出: {} \n" \
                       "总和为: {}".format(sender, text, str(result), str(sum([sum(i) for i in result])))
        except Exception:
            pass

@bot.register(msg_types=wxpy.TEXT)
def entrypoint(msg):
    if msg.text.startswith(".r"):
        return roll_dice(msg)
    elif msg.text == '.help':
        return help(msg)

@bot.register(msg_types=wxpy.FRIENDS)
def add_friends(msg):
    new_friend = msg.card.accept()
    new_friend.send(HELP_TEXT)

bot.join()