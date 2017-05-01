import requests
import os
import jinja2

HEWEATHER_KEY = os.getenv("HEWEATHER_KEY")

WEATHER_FORECAST_API = 'https://free-api.heweather.com/v5/forecast?city={city}&key=' + HEWEATHER_KEY
WEATHER_API = 'https://free-api.heweather.com/v5/weather?city={city}&key=' + HEWEATHER_KEY

def fetch_weather_forecast(city):
    resp = requests.get(WEATHER_FORECAST_API.format(city=city))
    return resp.json()

def fetch_weather(city):
    resp = requests.get(WEATHER_API.format(city=city))
    return resp.json()

def _parse_forecast(data, n):
    day = data['HeWeather5'][0]['daily_forecast'][n]
    return {"day_cond_d": day['cond']['txt_d'],
            "day_cond_n": day['cond']['txt_n'],
            "day_tmp_max": day['tmp']['max'],
            "day_tmp_min": day['tmp']['min']}

WEATHER_TEMPLATE = jinja2.Template(
"{{city}} 天气\n{% for item in items %}"
"{% if loop.index == 1 %}今天:{% endif %}"
"{% if loop.index == 2 %}明天:{% endif %}"
"{% if loop.index == 3 %}后天:{% endif %}"
" {% if item.day_cond_d|string() == item.day_cond_n|string() -%}"
"{{item.day_cond_n}} {%- else -%} {{item.day_cond_d}} 转 {{item.day_cond_n}} {%- endif -%},"
"最高 {{item.day_tmp_max}} 度, 最低 {{item.day_tmp_min}} 度\n{% endfor -%}"
)

def get_weather_forecast_msg(city_str):
    data = fetch_weather_forecast(city_str)
    if data['HeWeather5'][0].get('status') == "unknown city":
        return "您要找的城市不在地球上"
    city = data['HeWeather5'][0]['basic']['city']
    items = [_parse_forecast(data, i) for i in range(3)]
    return WEATHER_TEMPLATE.render(city=city,
                                   items=items)
AQI_TEMPLATE = jinja2.Template(
"{{city}} 空气质量\n"
"AQI: {{aqi}} {{qlty}}\n"
"PM2.5: {{pm25}}\n"
"PM10: {{pm10}}\n"
"CO: {{co}}\n"
"NO2: {{no2}}\n"
"O3: {{o3}}\n"
"PM10: {{pm10}}"
)

def get_aqi_msg(city_str):
    data = fetch_weather(city_str)
    if data['HeWeather5'][0].get('status') == "unknown city":
        return "您要找的城市不在地球上"
    city = data['HeWeather5'][0]['basic']['city']
    aqi = data['HeWeather5'][0]["aqi"]['city']
    return AQI_TEMPLATE.render(city=city, **aqi)

if __name__ == '__main__':
    print(get_weather_forecast_msg("shanghai"))
    print(get_aqi_msg("shanghai"))