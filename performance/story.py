#story with anime
import random
import animation_class as anime
import sys

def some_story():
    spacex = anime.myhand()
        
    steve = anime.human("steve", "male")
    annie = anime.human("annie", "female")
    stranger = anime.human("( ͡° ͜ʖ ͡°)", 'male')
    kate = anime.human("kate", "female")

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

def create_random(space, true_center, names=[]):
    humans = []
    for key, name in enumerate(names):
        center=(random.randrange(150, 1266), random.randrange(200, 668))
        center = true_center #(660, 400)
        human = anime.human(name, "male")
        human.setCenter(space, center)
        human.makePart(space)
        human.move(space, 'down', 1)
        if key%2 == 0:
            #human.move(space, 'up', 2)
            human.move(space, 'right', 20 + 80*key)
            human.move(space, 'down', 20)
        else:
            #human.move(space, 'down', 2)
            human.move(space, 'left', 20 + 80*key)       
        humans.append(human)
    return humans   
    
def main():
    nicks = '''some, one, else'''
    to_call = " ".join(["@" + item.strip() for item in nicks.split(",")])
    humans_names = [item.strip() for item in nicks.split(',')]
    print(humans_names)
    
    #humans_names = ["steve" + str(x) for x in range(2500)]
    spacex = anime.myhand()
    humans_all = create_random(space=spacex, true_center=(600, 200), names=humans_names[:])
    #humans_all = create_random(space=spacex, true_center=(600, 200), names=humans_names[:5])
    #humans_all = create_random(space=spacex, true_center=(660, 300), names=humans_names[5:10])
    #humans_all = create_random(space=spacex, true_center=(720, 400), names=humans_names[10:15])
    #humans_all = create_random(space=spacex, true_center=(780, 500), names=humans_names[15:20])
    the_one = humans_all[0]
    the_one.say_something(spacex, "some title")
    the_one.move(spacex, 'up', 1)
    
    
    '''
    spacex = anime.myhand()
    row_number = 4
    humans_01 = create_humans(space=spacex, number=row_number, center=(650,200))
    humans_02 = create_humans(space=spacex, number=row_number, center=(680,230))
    humans_03 = create_humans(space=spacex, number=row_number, center=(650,260))
    humans_04 = create_humans(space=spacex, number=row_number, center=(680,290))
    out = [human.move(spacex, 'left', 200) for human in humans_01]    
    out = [human.move(spacex, 'right', 200) for human in humans_02]
    out = [human.move(spacex, 'left', 225) for human in humans_03]
    out = [human.move(spacex, 'right', 225) for human in humans_04]
    '''
    
if __name__ == "__main__":
    main()
    #some_story()
    