# Bot
一个智障的微信机器人，有很多奇奇怪怪的功能

demo:

![qrcode](qrcode.jpeg)

## Run
```bash
export HEWEATHER_KEY="your heweather key"
python bot.py
```

## Usage

### 掷骰子
给bot发如下消息可以掷骰子。适用于 TRPG 跑团 (DnD, CoC, etc.) 

基础用法，d 前面的数字为掷的次数，后面的数字为骰子面数，下面的即为投 2 次 6 面骰子。

```
.r 2d6
```

可以一次掷多种骰子，用加号连接即可

```
.r 1d6+1d20
```

可以增加修正值，在中间直接加减相应的数字

```
.r 1d6+5d20-10
```

可以在骰子语句后空格，然后写一句本次掷骰的用处（描述）

```
.r 1d100 群主今天女装的概率
```

### 天气及空气质量

查询天气

```
.tq 上海
```

```
.tq beijing
```

查询空气质量

```
.aqi 上海 
```

```
.aqi beijing
```