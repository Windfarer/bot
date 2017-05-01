import random
import re

dice_pattern = re.compile(r'''([+-]{0,1}(\d+)[Dd](\d+))|([+-]{0,1}(\d+))''')

def roll(text, limit=1000):
    groups = dice_pattern.findall(text)
    if len(groups) > limit:
        return []
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
        result.append(sub_result)
    return result