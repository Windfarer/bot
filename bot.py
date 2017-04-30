import random
import wxpy
import re

dice_pattern = re.compile(r'''([+-]{0,1}(\d+)[Dd](\d+))|([+-]{0,1}(\d+))''')

def roll(text):
    groups = dice_pattern.findall(text)
    result = []
    for group in groups:
        if group[0]:
            if group[0].startswith('-'):
                sign = -1
            else:
                sign = 1
            for i in range(int(group[1])):
                result.append(sign * random.randint(1, int(group[2])))
        elif group[3]:
            result.append(int(group[3]))
    return result


bot = wxpy.Bot(console_qr=True, cache_path='/data/wxpy.pkl')

group = bot.groups()

@bot.register(chats=bot.groups()+bot.friends())
def roll_dice(msg):
    if msg.type == wxpy.TEXT and msg.text.startswith(".r"):
        sender = msg.member.name
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
        
bot.join()