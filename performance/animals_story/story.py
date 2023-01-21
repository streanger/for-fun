import sys
import os
import random

# 3rd party
import numpy as np
import winsound

# my modules
import check_gender_by_nick
import animation_class as anime
from alpha_image import alpha_image
from wykop_avatars import convert_nick_str_to_list, save_avatars


def script_path():
    '''change current path to script one'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    return path

def make_dir(new_dir):
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = os.path.join(path, new_dir)
    return new_path    
    
def some_story():
    spacex = anime.myhand(bg_color="blue", line_size=3)
        
    steve = anime.human("steve", "male", '')
    annie = anime.human("annie", "female", '')
    stranger = anime.human("( ͡° ͜ʖ ͡°)", 'male', '')
    kate = anime.human("kate", "female", '')

    #open curtain
    kate.makeDecoration(spacex)
    kate.openCurtain(spacex, openSpeed="fast")

    steve.makePart(spacex)
    annie.makePart(spacex)
    annie.move(spacex, 'right', 30)
    annie.move(spacex, 'right', 90)
    annie.move(spacex, 'forward', 30)
    annie.move(spacex, 'x', 30)
    steve.move(spacex, 'x', 30)
    steve.move(spacex, 'x', 30)

    stranger.setCenter(spacex, center=True)
    stranger.makePart(spacex)
    stranger.move(spacex, "left", 30)
    steve.move(spacex, "right", 30)
    steve.move(spacex, 'x', 30)
    stranger.move(spacex, "right", 30)
    stranger.move(spacex, "right", 30)
    stranger.move(spacex, "right", 30)

    kate.setCenter(spacex, [450,285])
    kate.makePart(spacex)
    kate.move(spacex, 'up', 30)
    kate.move(spacex, 'up', 30)
    kate.move(spacex, 'left', 30)
    kate.move(spacex, 'forward', 80)
    kate.move(spacex, 'right', 120)

    for x in range(4):
        stranger.move(spacex, "up", 30)
        stranger.move(spacex, "down", 30)
        kate.move(spacex, 'up', 30)
        kate.move(spacex, 'down', 30)

    #spacex.canvas.delete("all")	
        
    #close curtain
    kate.makeDecoration(spacex, full=False)
    kate.openCurtain(spacex, openSpeed="fast", direct="close")


    #wtf
    stranger.setCenter(spacex, [100,200])
    stranger.makePart(spacex)
    movement = '4444333333324242424111111111111'
    for moves in movement:
        for move in moves:
            stranger.move(spacex, str(move), 30)

    print("works fine")
    
def create_humans(space, number, center, name="steve"):
    humans = []
    for x in range(number):
        human = anime.human(name + str(x), "male")
        human.setCenter(space, center)
        human.makePart(space)
        human.move(space, 'down', 200)
        #for y in range(2*x):
        #human.move(space, 'down', 5*x)
        if x%2 == 0:
            #human.move(space, 'up', 2)
            human.move(space, 'right', 15 + 30*x)
        else:
            #human.move(space, 'down', 2)
            human.move(space, 'left', 15 + 30*x)
        humans.append(human)
    return humans

def create_random(space, true_center, names):
    humans = []
    centers = []
    for key, (nick, face_img) in enumerate(names.items()):
        '''
        while True:
            center=(random.randrange(50, 1300), random.randrange(200, 608))
            if input('center ok: {}? nick: {} (Yes/no)'.format(center, nick)).lower() != 'no':
                break
        '''
        center = true_center #(660, 400)
        #center=(random.randrange(50, 1300), random.randrange(200, 608))
        
        
        #face_img = random.choice(["fizzix.png", "forch.png", "berk.png", "Fortyk.png", "fojteqkloc.png", ""])
        sex, _ = check_gender_by_nick.check_sex(nick)       #it returns tuple
        # human = anime.human(nick, sex, face_img)
        human = anime.human(nick, 'monster', face_img)
        human.setCenter(space, center)
        if True:
            human.makePart(space)
            human.move(space, 'down', 1)
            if key%2 == 0:
                #human.move(space, 'up', 2)
                human.move(space, 'right', 0 + 0*key)
                human.move(space, 'down', 0)
            else:
                #human.move(space, 'down', 2)
                human.move(space, 'left', 0 + 0*key)
            while False:
                if input('move anon: {} (yes/No)?\n'.format(nick)).lower() == 'yes':
                    to_move = (input('make move (e.g. left 10):\n')).split()
                    side = to_move[0]
                    value = int(to_move[1])
                    human.move(space, side, value)
                else:
                    break        
        humans.append(human)
    return humans
    
def main():
    path = script_path()
    nicks = '''some, one, else'''
    nicks = '''some'''
    args = sys.argv[1:]
    pngFiles = [item for item in args if item.endswith('.png')]
    if not pngFiles:
        images_path = 'images'
        pngFiles = [os.path.join(images_path, item) for item in os.listdir(images_path) if item.endswith('.png')]
    # print(pngFiles)
    imgPath = random.choice(pngFiles)
    if not imgPath:
        return False
    # to_call = " ".join(["@" + item.strip() for item in nicks.split(",")])
    # humans_names = [item.strip() for item in nicks.split(',')]
    humans_names = {item.strip():imgPath for item in nicks.split(',')}

    spacex = anime.myhand(bg_color="black", line_size=2)
    screenHeight = spacex.screenHeight
    creator = anime.human('creator', 'male', '')        #creator itself
    #creator.makeDecoration(spacex)
    creator.make_ground(spacex, level=90)


    humans_all = create_random(space=spacex, true_center=(200, screenHeight-170-170), names=humans_names)
    the_one = humans_all[0]
    
    if 'r' in os.path.basename(sys.argv[0]):
        randomMode = True
    else:
        randomMode = False
    
    if 'q' in os.path.basename(sys.argv[0]):
        quietMode = True
    else:
        quietMode = False
    # print('randomMode:', randomMode)
    
    while True:
    # for x in range(0):
        for the_one in humans_all:
            if not quietMode:
                winsound.PlaySound('sounds/smb_jump.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
            if randomMode:
                random_jump_pig(spacex, the_one)
            else:
                the_one.jump(spacex, 100, 40, 5)
                the_one.jump(spacex, 100, 80, 5)
                the_one.jump(spacex, 100, 160, 5)
                the_one.jump(spacex, 100, 250, 5)
                # the_one.jump(spacex, 100, 250, 5)
                the_one.jump(spacex, 100, 250, -5)
                the_one.jump(spacex, 100, 160, -5)
                the_one.jump(spacex, 100, 80, -5)
                the_one.jump(spacex, 100, 40, -5)
                

def random_jump(space, jumper):    
    rand_speed = random.randrange(10, 100)
    rand_high = random.randrange(600)
    current_position = jumper.get_position(space)[0]
    if current_position > (space.screenWidth)-100:
        rand_dist = random.randrange(-20, 0)
    elif current_position < 100:
        rand_dist = random.randrange(20)
    else:
        rand_dist = random.randrange(-20, 20)
    print("current_position(x): {}, speed: {}, high: {}, distance: {}".format(current_position, rand_speed, rand_high, rand_dist))
    jumper.jump(space, rand_speed, rand_high, rand_dist)
    return True

def random_jump_pig(space, jumper):    
    rand_speed = random.randrange(20, 100)
    rand_high = random.randrange(300)
    current_position = jumper.get_position(space)[0]
    if current_position > (space.screenWidth)-100:
        rand_dist = random.randrange(-20, 0)
    elif current_position < 100:
        rand_dist = random.randrange(20)
    else:
        rand_dist = random.randrange(-20, 20)
    # print("current_position(x): {}, speed: {}, high: {}, distance: {}".format(current_position, rand_speed, rand_high, rand_dist))
    jumper.jump(space, rand_speed, rand_high, rand_dist)
    return True    
    
def vikop_story():
    path = script_path()
    nicks = """@Arveit @Raptorini @Marterr_ @s0msiad @Kulturalny_Jegomosc90 @milicja @Slacky @Faiko @7845 @namzio"""
    nick_list, to_call = convert_nick_str_to_list(nicks)
    avatars_paths = save_avatars(nick_list, subdir='avatars')       #in normal size
    avatars_paths = {key: alpha_image(value, 80, 80, 'circle_avatars') for key, value in avatars_paths.items()}     #resize, circle, alpha channel
    humans_names = list(avatars_paths.keys())
    print(humans_names)
    
    spacex = anime.myhand(bg_color="black", line_size=2)
    screenHeight = spacex.screenHeight
    creator = anime.human('creator', 'male', '')        #creator itself
    #creator.makeDecoration(spacex)
    creator.make_ground(spacex, level=90)
    #creator.say_something(spacex, "armia przegrywów V2.0")
    
    humans_all = create_random(space=spacex, true_center=(200, screenHeight-170), names=avatars_paths)
    #for x in range(40):
    while True:
        for key, the_one in enumerate(humans_all):
            random_jump(spacex, the_one)
            # the_one.jump(spacex, 20, 40, 5)
            # the_one.jump(spacex, 10, 80, 5)
            # the_one.jump(spacex, 100, 560, 10+key)
            # the_one.jump(spacex, 100, 250, 20)
            # the_one.jump(spacex, 100, 250, -20+key)
            # the_one.jump(spacex, 20, 160, -10)
            # the_one.jump(spacex, 100, 80, -5)
            # the_one.jump(spacex, 100, 40, -5)
    
    #download avatars
    #convert avatars size and alpha; save it to specified dir
    #create humans
    #write scenario
    

if __name__ == "__main__":
    # vikop_story()  # won't work due to wrong avatars request parsing
    main()  # work quite fine
    # some_story()  # won't work correctly due to some animation class changes

'''    
todo:
    -resize image +
    -cut circle +
    -make alpha channel +
    -add 'say' method with clouds
    -prevent overwriting avatars image in directory
'''