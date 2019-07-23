import random


def parse_pool(raw):
    pool = {"num": 1, "sides": 1, "mod": 0}
    
    raw = raw.lower().strip().split("d")
    num, sides, mod = "1", "1", "0"
    
    if "+" in raw[-1]:
        sides, mod = raw[-1].split("+")
        
    elif "-" in raw[-1]:
        sides, mod = raw[-1].split("-")
        mod = -mod
    else:
        sides = int(raw[-1])
        
    num = int(raw[0])
    pool["num"] = num
    pool["sides"] = int(sides)
    pool["mod"] = int(mod)
    
    return pool
    
def roll_pool(pool):
    result = 0
    
    for i in range(pool['num']):
        result += random.randint(1, pool['sides'])
        
    result += pool['mod']
    return result
    
    # elif "-" in raw