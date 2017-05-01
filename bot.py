import wxpy
import jinja2
from roll import roll
from weather import get_weather_forecast_msg, get_aqi_msg

bot = wxpy.Bot(console_qr=True, cache_path='/data/wxpy.pkl')

group = bot.groups()

HELP_TEXT = "使用说明:\n" \
            "【.r 骰子个数d面数】" \
            "如 .r 2d6 即为掷2个6面骰子\n" \
            "【.tq 城市】查询天气\n" \
            "【.aqi 城市】查询空气质量"

def help(msg):
    return HELP_TEXT

def roll_dice(msg):
    sender = msg.member.name if msg.member else msg.sender.name
    text = msg.text[2:].strip()
    print(text)
    result = roll(text.split(" ", 2)[0])
    if result:
        print(result)
        return "{} 掷了骰子「 {} 」\n" \
               "掷出: {} \n" \
               "总和为: {}".format(sender, text, str(result)[1:-1], str(sum([sum(i) for i in result])))

def get_weather_forecast(msg):
    city_str = msg.text[4:].strip()
    return get_weather_forecast_msg(city_str=city_str)

def get_aqi(msg):
    city_str = msg.text[5:].strip()
    return get_aqi_msg(city_str)

@bot.register(msg_types=wxpy.TEXT)
def entrypoint(msg):
    if msg.text.startswith(".r "):
        return roll_dice(msg)
    if msg.text.startswith(".tq "):
        return get_weather_forecast(msg)
    if msg.text.startswith(".aqi "):
        return get_aqi(msg)
    elif msg.text == '.help':
        return help(msg)

@bot.register(msg_types=wxpy.FRIENDS)
def add_friends(msg):
    new_friend = msg.card.accept()
    new_friend.send(HELP_TEXT)

bot.join()