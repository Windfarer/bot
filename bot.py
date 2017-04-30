import random
import wxpy
import re

dice_pattern = re.compile(r'''([+-]{0,1}(\d+)[Dd](\d+))|([+-]{0,1}(\d+))''')

def roll(text, limit=1000):
    groups = dice_pattern.findall(text)
    result = []
    for group in groups:
        if group[0]:
            if group[0].startswith('-'):
                sign = -1
            else:
                sign = 1
            for i in range(int(group[1])):
                n = int(group[2])
                if n > limit:
                    return []
                result.append(sign * random.randint(1, n))
        elif group[3]:
            result.append(int(group[3]))
    return result


bot = wxpy.Bot(console_qr=True, cache_path='/data/wxpy.pkl')

group = bot.groups()

def help(msg):
    return ".r 骰子个数d面数，\n" \
           "如「 .r 2d6 」即为掷2个6面的骰子"

def roll_dice(msg):
    if msg.type == wxpy.TEXT and msg.text.startswith(".r"):
        sender = msg.member.name if msg.member else msg.sender.name
        text = msg.text[2:].strip()
        try:
            result = roll(text)
            if result:
                print(result)
                return "{} 掷了骰子「 {} 」\n" \
                       "掷出: {} \n" \
                       "总和为: {}".format(sender, text, str(result), str(sum(result)))
        except Exception:
            pass

@bot.register(chats=bot.groups()+bot.friends())
def entrypoint(msg):
    if msg.type == wxpy.TEXT and msg.text.startswith(".r"):
        return roll_dice(msg)
    elif msg.type == wxpy.TEXT and msg.text == '.help':
        return help(msg)

bot.join()