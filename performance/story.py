#story with anime
import animation_class as anime

def some():
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
    annie.move(spacex, 'right')
    annie.move(spacex, 'right')
    annie.move(spacex, 'forward')
    annie.move(spacex)
    steve.move(spacex)
    steve.move(spacex)

    stranger.setCenter(spacex, center=True)
    stranger.makePart(spacex)
    stranger.move(spacex, "left")
    steve.move(spacex, "right")
    steve.move(spacex)
    stranger.move(spacex, "right")
    stranger.move(spacex, "right")
    stranger.move(spacex, "right")

    kate.setCenter(spacex, [450,285])
    kate.makePart(spacex)
    kate.move(spacex, 'up')
    kate.move(spacex, 'up')
    kate.move(spacex, 'left')

    for x in range(4):
        stranger.move(spacex, "up")
        stranger.move(spacex, "down")
        kate.move(spacex, 'up')
        kate.move(spacex, 'down')

    #spacex.canvas.delete("all")	
        
    #close curtain
    kate.makeDecoration(spacex, full=False)
    kate.openCurtain(spacex, openSpeed="normal", direct="close")


    #wtf
    stranger.setCenter(spacex, [100,200])
    stranger.makePart(spacex)
    movement = '4444333333324242424111111111111'
    for moves in movement:
        for move in moves:
            stranger.move(spacex, str(move))

    print("works fine")
    
def create_humans(space, number, center):
    humans = []
    for x in range(number):
        human = anime.human("steve" + str(x), "male")
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
        
if __name__ == "__main__":
    row_number = 10
    spacex = anime.myhand()
    humans_01 = create_humans(space=spacex, number=row_number, center=(660,200))
    humans_02 = create_humans(space=spacex, number=row_number, center=(680,225))
    humans_03 = create_humans(space=spacex, number=row_number, center=(660,250))
    humans_04 = create_humans(space=spacex, number=row_number, center=(680,275))
    out = [human.move(spacex, 'left', 200) for human in humans_01]    
    out = [human.move(spacex, 'right', 200) for human in humans_02]
    out = [human.move(spacex, 'left', 225) for human in humans_03]
    out = [human.move(spacex, 'right', 225) for human in humans_04]
    
        
