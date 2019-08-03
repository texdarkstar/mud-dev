import random


# humanoid = {
    # 'head': 5,
    # 'left arm': 10,
    # 'right arm': 10,
    # 'body': 45,
    # 'left leg': 15,
    # 'right leg': 15,
# }
human = {
    'head': 5,
    'hands': 20,
    'body': 45,
    'legs': 30,
}
wolf = {
    'head': 5,
    'paws': 15,
    'body': 40,
    'legs': 40,
}
orc = {
    'head': 5,
    'hands': 20,
    'body': 45,
    'legs': 30,
}    

human_table = []
wolf_table = []


races = {
        "human": [human, human_table],
        "wolf": [wolf, wolf_table],

    }


def build_tables():
    for race in races.keys():
        for hitbox in races[race][0]:
            for i in range(races[race][0][hitbox]):
                races[race][1].append(hitbox)


def roll_location(race):
    return random.choice(races[race][1])



build_tables()
