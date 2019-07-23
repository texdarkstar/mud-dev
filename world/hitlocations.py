import random


# humanoid = {
    # 'head': 5,
    # 'left arm': 10,
    # 'right arm': 10,
    # 'body': 45,
    # 'left leg': 15,
    # 'right leg': 15,
# }
humanoid = {
    'head': 5,
    'hands': 20,
    'body': 45,
    'legs': 30,
}
quadruped = {
    'head': 5,
    'hands': 15,
    'body': 40,
    'legs': 40,
}


humanoid_table = []
quadruped_table = []

bodytypes = {
        "humanoid": [humanoid, humanoid_table],
        "quadruped": [quadruped, quadruped_table],
    }


def build_tables():
    for bodytype in bodytypes.keys():
        for hitbox in bodytypes[bodytype][0]:
            for i in range(bodytypes[bodytype][0][hitbox]):
                bodytypes[bodytype][1].append(hitbox)


def roll_location(bodytype):
    return random.choice(bodytypes[bodytype][1])



build_tables()
