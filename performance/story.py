#story with anime
import twoclass06 as anime

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
