import random

avatar_angry = [
    "/static/angry_trex.png",
    "/static/angry_triceratops.png",
    "/static/angry_head_dino.png",
]

avatar_happy = [
    "/static/happy_blue_dino.png",
    "/static/happy_fly_dino.png",
    "/static/happy_stego.png",
]

def give_avatar(type:str)->str:
    if type == "happy":
        return random.choice(avatar_happy)
    if type == "angry":
        return random.choice(avatar_angry)
    else: 
        return None