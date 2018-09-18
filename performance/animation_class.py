#this is takemyhand script
#font styles: normal, bold, roman, italic, underline, over, strike; combinations-> "bold italic"
#arc styles: "arc" "pieslice" "chord"
#skin color: #ffe6b3


#some sound would be usefull
from tkinter import *
import time
import random
# from PIL import ImageGrab, Image
import os
import sys
import cv2
import numpy as np

'''    
todo:
    -rezie image +
    -cut circle +
    -make alpha channel +
    -add 'say' method with clouds
    -prevent overwriting avatars image in directory
'''

def script_path():
    '''change current path to script one'''
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path

class human:

    def __init__(self, name, sex, face_img):
        self.name = name
        self.sex = sex

        #self.file = random.choice(["fizzix.png", "forch.png", "berk.png", "Fortyk.png", "fojteqkloc.png"])
        self.file = face_img
        # self.file = "2.png"
        #self.image = PhotoImage(file=self.file, master = self.space, width = 150, height = 150)
        if self.file:
            # self.image = PhotoImage(file=self.file, width = 150, height = 150)
            self.image = PhotoImage(file=self.file, width = 510, height = 510)
        else:
            self.image = ""
        
    def makePart(self, spacex):
        if (self.sex == "male"):
            self.rightshoe = spacex.createShoes(vx=-1)
            self.leftshoe = spacex.createShoes(vx=1)
            self.rightleg = spacex.createLeg(vx=-1)
            self.leftleg = spacex.createLeg(vx=1)
            self.body = spacex.createBody()
            self.head = spacex.createHead(img=self.image)
            # self.humanname = spacex.printName(self.name)    
            self.humanname = spacex.printName('')    
        elif (self.sex == "female"):
            self.rightshoe = spacex.createShoes(vx=-1)
            self.leftshoe = spacex.createShoes(vx=1)
            self.rightleg = spacex.createLegF(vx=-1)
            self.leftleg = spacex.createLegF(vx=1)
            self.body = spacex.createBodyF()
            self.head = spacex.createHeadF(img=self.image)
            self.humanname = spacex.printName(self.name)
        else:
            print('what kind of monster is this?')
            # self.rightshoe = spacex.createShoes(vx=-1)
            # self.leftshoe = spacex.createShoes(vx=1)
            # self.rightleg = spacex.createLegF(vx=-1)
            # self.leftleg = spacex.createLegF(vx=1)
            # self.body = spacex.createBodyF()
            self.head = spacex.createHead(img=self.image)
        self.parts = [self.head]
                      
    def move(self, spacex, direction, steps):
        spacex.movePart(self.parts, direction, steps)    
    
    def jump(self, spacex, a_factor, b_factor, step):
        spacex.jump(self.parts, a_factor, b_factor, step)
    
    def get_position(self, spacex):
        return spacex.parts_position(self.parts)
    
    def say_something(self, spacex, some_text):
        spacex.putTitle(some_text)
    
    def setCenter(self, spacex, pcen=[100,100], center=False):
        spacex.setpcen(pcen, center)
    
    def makeDecoration(self, spacex, full=True ):
        #to refactoring in free time
        #przyciemnienie, rozjaśnianie ?
        if (full == False):
            self.leftcurtain = spacex.createCurtainOpened(vx=-1,vy=0)
            self.rightcurtain = spacex.createCurtainOpened(vx=1,vy=0)
        elif (full == True):
            self.ground = spacex.createGround()
            self.leftcurtain = spacex.createCurtain(vx=0, vy=0)
            self.rightcurtain = spacex.createCurtain(vx=1, vy=0)    
        self.decoration = [self.leftcurtain,
                           self.rightcurtain]            
    
    def make_ground(self, spacex, level):
        self.ground = spacex.make_ground(level)
    
    def openCurtain(self, spacex, openSpeed="normal", direct="open"):
        spacex.openCurtain(self.decoration, openSpeed, direct)
    
    
class myhand:
    
    def __init__(self, bg_color, line_size):
        #make canvas
        if False:
            self.screenWidth = 1920
            self.screenHeight = 1080
        else:
            self.screenWidth = 1366
            self.screenHeight = 768            
        #self.screenWidth = 600
        #self.screenHeight = 400
        self.space = Tk()
        #self.space = Toplevel()
        self.canvas = Canvas(self.space, width=self.screenWidth, height=self.screenHeight)
        self.canvas.config(bg=bg_color)
        self.canvas.pack()
        #mirroring reverse
        self.vx, self.vy = 1, 1
        self.x, self.y = 1, 1
        #center of the view
        self.centerx, self.centery = 300, 225
        #person center; variable
        self.pcen = [120,120]
        #font atributes
        self.font = ('times', 14, 'bold')
        self.path = script_path()
        self.line_size = line_size
        
    def setFont(self, family="times", fontsize=15, fontstyle='bold'):
        self.font = (family,fontsize,fontstyle)
    
    def putTitle(self, title="some_title"):
        self.canvas.create_text(680,30,fill="blue",font="Times 40 italic bold", text=title)
    
    def movePart(self, parts, direct="down", steps=10):
        if (direct=="forward"):
            x,y = 1,2
        elif (direct=="back"):
            x,y = -1,-2
        elif (direct=="right") or (direct=='3'):
            x,y = 1,0
        elif (direct=="left") or (direct=='1'):
            x,y = -1,0    
        elif (direct=="up") or (direct=='2'):
            x,y = 0,-1
        elif (direct=="down") or (direct=='4'):
            x,y = 0,1
        elif (direct=="x"):
            x,y = 1,1
        else:
            x,y = 1,1
        for i in range(steps):
            time.sleep(0.0001)
            for part in parts:
                #this is for iterating throughout all elements in parts
                try:
                    for element in part:
                        #print(element)
                        self.canvas.move(element, x, y)    #just part not every single thing
                        self.canvas.pack()
                        self.canvas.update()
                except:
                    #print(part)
                    self.canvas.move(part, x, y)    #just part not every single thing
                    self.canvas.pack()
                    self.canvas.update()
    
    def parts_position(self, parts):
        '''get mean positions of all parts'''
        all_coords = []
        for part in parts:
            all_coords.extend(self.canvas.coords(part))
            #print(part, self.canvas.coords(part))
        all_coords = np.reshape(all_coords, (-1, 2))
        x_pos, y_pos = [np.mean(item) for item in zip(*all_coords)]
        return x_pos, y_pos
            
    def jump(self, parts, a_factor, b_factor, step):
        jump_path = [round(-a_factor*((x*0.1)**2)+b_factor) for x in range(-b_factor, b_factor)]
        jump_path = [item for item in jump_path if item > 0]
        jump_path = [item - jump_path[key-1] for key, item in enumerate(jump_path) if key > 0]
        for key, value in enumerate(jump_path):
            time.sleep(0.02)
            for part in parts:
                #this is for iterating throughout all elements in parts
                try:
                    for element in part:
                        #print(element)
                        self.canvas.move(element, step, -value)    #just part not every single thing
                        self.canvas.pack()
                        self.canvas.update()
                except:
                    #print(part)
                    self.canvas.move(part, step, -value)    #just part not every single thing
                    self.canvas.pack()
                    self.canvas.update()
            #file = "shot_" + str(round(time.time(),4)*10000) + ".jpg"
            #file_path = os.path.join("animation", file)
            #ImageGrab.grab((30,100,1000,700)).save(file_path)
            #time.sleep(0.001)
            #input("key {} value {}".format(key, value))
    
    def setCenter(self, xpoint, ypoint):
        self.centerx = xpoint
        self.centery = ypoint
        if (xpoint > 600):
            self.centerxt = 600
        if (ypoint > 450):
            self.centery = 225
            
    def drawThing(self):
        print(42)
        if (self.sex == "male"):    
            self.drawleftleg = self.createLeg(vx=1)
            self.drawrightleg = self.createLeg(vx=-1)
            self.drawleftshoe = self.createShoes(vx=1)
            self.drawrightshoe = self.createShoes(vx=-1)
            self.drawbody = self.createBody()
            self.drawhead = self.createHead()
        elif (self.sex == "female"):
            self.drawleftleg = self.createLeg(vx=0.8)
            self.drawrightleg = self.createLeg(vx=-0.8)
            self.drawleftshoe = self.createShoes(vx=0.5)
            self.drawrightshoe = self.createShoes(vx=-0.5)
            self.drawbody = self.createBody()
            self.drawhead = self.createHead()
        
    def saySomething(self, sentence="say"):
        #put this cloud above the man programaticallly
        self.cloud = self.canvas.create_oval(20,20,160,110, width=3, outline="#00ff00", fill="#eeffcc")
        self.littleTalk = self.canvas.create_text(90,60, text=sentence, font=self.font)
        
    def printName(self, name="name", vx=1,vy=1):
        self.vx = vx
        self.vy = vy
        return self.canvas.create_text(self.pcen[0],self.pcen[1]-20, text=name, font=self.font, fill=random.choice(["white", "purple", "green", "yellow", "blue"]))
        
    def createLeg(self, vx=1,vy=1):
        self.vx = vx
        self.vy = vy
        manleg = self.canvas.create_polygon(self.pcen[0], self.pcen[1],
                                            self.pcen[0]-20*self.vx, self.pcen[1], 
                                            self.pcen[0]-10*self.vx, self.pcen[1]+70*self.vy, 
                                            self.pcen[0], self.pcen[1]+70*self.vy,  
                                            outline="white", fill="black", width=self.line_size)
        return manleg
        
    def createLegF(self, vx=1,vy=1):
        self.vx = vx
        self.vy = vy
        womanleg = self.canvas.create_polygon(self.pcen[0],self.pcen[1]+40,
                                              self.pcen[0]-13*self.vx,self.pcen[1]+40,
                                              self.pcen[0]-8*self.vx,self.pcen[1]+70*self.vy,
                                              self.pcen[0],self.pcen[1]+70*self.vy,
                                              outline="white",fill="#ffe6b3", width=self.line_size)
        return womanleg
    
    def createHead(self, img, vx=1, vy=1):
        self.vx = vx
        self.vy = vy
        if img:
            # head = self.canvas.create_image(self.pcen[0]-40,self.pcen[1]-130,image=img,anchor=NW)
            head = self.canvas.create_image(self.pcen[0]-240,self.pcen[1]-230,image=img,anchor=NW)
        else:
            head =  self.canvas.create_oval(self.pcen[0]-20,self.pcen[1]-100,self.pcen[0]+20,self.pcen[1]-60, outline="yellow", fill='#ffe6b3')
        return head
        
    def createHeadF(self, img, vx=1, vy=1):
        self.vx = vx
        self.vy = vy
        if img:
            #something
            head = self.canvas.create_image(self.pcen[0]-40,self.pcen[1]-130,image=img,anchor=NW)
            return head
        else:
            head =  self.canvas.create_oval(self.pcen[0]-20,self.pcen[1]-100,self.pcen[0]+20,self.pcen[1]-60, outline="yellow", fill='#ffe6b3')
            
            hairline01 = (self.pcen[0]-25, self.pcen[1]-105, self.pcen[0]+13, self.pcen[1]-70 )
            hairline02 = (self.pcen[0]+25, self.pcen[1]-105, self.pcen[0]-13, self.pcen[1]-70)
            hairline03 = (self.pcen[0]-20, self.pcen[1]-100, self.pcen[0]+13, self.pcen[1]-70)
            hairline04 = (self.pcen[0]-15, self.pcen[1]-95, self.pcen[0]+13, self.pcen[1]-70)
            hair01 = self.canvas.create_arc(hairline01, start=20, extent=220, fill="red", outline="white", width=3)
            hair02 = self.canvas.create_arc(hairline02, start=-40, extent=150, fill="red", outline="yellow", width=3)
            hair03 = self.canvas.create_arc(hairline03, start=60, extent=150, outline="#66ff66", width=2, style="arc")
            hair04 = self.canvas.create_arc(hairline04, start=60, extent=150, outline="#66ff66", width=2, style="arc")
            return head, hair01, hair02, hair03, hair04    
    
    def createShoes(self, vx=1, vy=1):
        self.vx = vx
        self.vy = vy
        return self.canvas.create_polygon(self.pcen[0],self.pcen[1]+70,self.pcen[0]-10*self.vx,self.pcen[1]+70,
                                          self.pcen[0]-20*self.vx,self.pcen[1]+75,self.pcen[0]-20*self.vx,self.pcen[1]+80,
                                          self.pcen[0],self.pcen[1]+80,self.pcen[0],self.pcen[1]+80,
                                          outline="white", fill="black", width=self.line_size)

    def createBody(self, vx=1, vy=1):    
        self.vx = vx
        self.vy = vy
        body = self.canvas.create_polygon(self.pcen[0]-20,self.pcen[1],
                                          self.pcen[0]-25,self.pcen[1]-30,
                                          self.pcen[0]-25,self.pcen[1]-40,
                                          self.pcen[0]-10,self.pcen[1]-45,
                                          self.pcen[0]+10,self.pcen[1]-45,
                                          self.pcen[0]+25,self.pcen[1]-40,
                                          self.pcen[0]+25,self.pcen[1]-30,
                                          self.pcen[0]+20,self.pcen[1]-0,
                                          outline="white", fill="black", width=self.line_size)
        return body
            
    def createBodyF(self, vx=1, vy=1):    
        self.vx = vx
        self.vy = vy
        body = self.canvas.create_polygon(self.pcen[0]-10,self.pcen[1]-45,
                                          self.pcen[0]-20,self.pcen[1]-40,
                                          self.pcen[0]-23,self.pcen[1]-25,
                                          self.pcen[0]-15,self.pcen[1]+10,
                                          self.pcen[0]+15,self.pcen[1]+10,
                                          self.pcen[0]+23,self.pcen[1]-25,
                                          self.pcen[0]+20,self.pcen[1]-40,
                                          self.pcen[0]+10,self.pcen[1]-45,
                                          outline="white", fill="black", width=self.line_size)
        skirt = self.canvas.create_polygon(self.pcen[0]-15,self.pcen[1]+10,
                                           self.pcen[0]-30,self.pcen[1]+45,
                                           self.pcen[0]+30,self.pcen[1]+45,
                                           self.pcen[0]+15,self.pcen[1]+10,
                                           outline="white", fill="black", width=self.line_size)
        coord = (self.pcen[0]-13, self.pcen[1]-62, self.pcen[0]+13, self.pcen[1]-27 )
        cleavage = self.canvas.create_arc(coord, start=180, extent=180, fill="#ffe6b3", outline="white", width=2, style="chord")
        blackline = self.canvas.create_line(self.pcen[0]-10,self.pcen[1]-46,
                                            self.pcen[0]+10,self.pcen[1]-46,
                                            fill="black", width=3)
        return body, skirt, cleavage, blackline
        
    def createGround(self, vx=1, vy=1):
        self.vx = vx
        self.vy = vy
        
        bluesky = self.canvas.create_polygon(0,0,
                                            self.screenWidth,0,
                                            self.screenWidth,self.screenHeight,
                                            0,self.screenHeight,
                                            fill="#b3ffff", width=self.line_size) 
        
        ground = self.canvas.create_polygon(0,self.screenHeight*0.9,
                                            self.screenWidth,self.screenHeight*0.9,
                                            self.screenWidth,self.screenHeight,
                                            0,self.screenHeight,
                                            fill="green", width=self.line_size)
        groundline = self.canvas.create_line(0,self.screenHeight*0.9,
                                            self.screenWidth,self.screenHeight*0.9,
                                            fill="brown", width=self.line_size)
                                            
        return groundline, ground, bluesky
    
    def make_ground(self, level):
        ground = self.canvas.create_polygon(0,self.screenHeight - level,
                                            self.screenWidth,self.screenHeight - level,
                                            self.screenWidth,self.screenHeight,
                                            0,self.screenHeight,
                                            fill="green", width=self.line_size)
        groundline = self.canvas.create_line(0,self.screenHeight - level,
                                            self.screenWidth,self.screenHeight - level,
                                            fill="brown", width=5)
        return ground, groundline
    
    def createCurtain(self, vx=0, vy=1):
        self.vx = vx
        self.vy = vy
        curtain = self.canvas.create_polygon(0+self.screenWidth*self.vx,0,
                                             (self.screenWidth/2),0,
                                             (self.screenWidth/2),self.screenHeight*0.89,
                                             0+self.screenWidth*self.vx,self.screenHeight*0.89,
                                             fill="purple", width=1)
        curtainLine = self.canvas.create_line((self.screenWidth/2),0,
                                              (self.screenWidth/2),self.screenHeight*0.89,
                                              fill="black", width=self.line_size)                                    
        return curtain, curtainLine
        
    def createCurtainOpened(self, vx=0, vy=1):
        self.vx = vx
        self.vy = vy
        curtain = self.canvas.create_polygon((self.screenWidth/2)*(1+2*self.vx),0,
                                              (self.screenWidth/2)*(1+1*self.vx),0,
                                              (self.screenWidth/2)*(1+1*self.vx),self.screenHeight*0.89,
                                              (self.screenWidth/2)*(1+2*self.vx),self.screenHeight*0.89,
                                              fill="purple", width=1)
        curtainLine = self.canvas.create_line((self.screenWidth/2)*(1+1*self.vx),0,
                                              (self.screenWidth/2)*(1+1*self.vx),self.screenHeight*0.89,
                                              fill="black", width=self.line_size)                                    
        return curtain, curtainLine
    
    def openCurtain(self, parts, openSpeed="normal", direct="open"):
        if (openSpeed == "normal"):
            timeWait = 0.01
        elif (openSpeed == "fast"):    
            timeWait = 0.001
        elif (openSpeed == "slow"):    
            timeWait = 0.1    
        else:
            timeWait = 0.01
        
        if (direct == "open"):
            x,y = 1, 0
        elif (direct == "close"):
            x,y = -1, 0
        else:
            x,y = 1, 0
            
        for i in range(int(self.screenWidth/2)):
            time.sleep(timeWait)
            for part in parts:
                for element in part:
                    if (parts.index(part) == 0):
                        self.canvas.move(element, -x, y)
                    else:
                        self.canvas.move(element, x, y)
                    self.canvas.pack()
                    self.canvas.update()    
        
    def setpcen(self, pcen=[150,150], center=False):
        if (center == True):
            #set person center in the center of the view
            self.pcen = [self.screenWidth/2, self.screenHeight/2]
        else:
            #in other way set it as user wish
            self.pcen = pcen
            
    
if __name__ == "__main__":
    spacex = myhand(bg_color="black", line_size=2)
    stranger = human("( ͡° ͜ʖ ͡°)", 'male', '')
    kate = human("kate", "female", '')
    kate.makeDecoration(spacex)
    kate.openCurtain(spacex, openSpeed="fast")
    
    stranger.setCenter(spacex, [100,200])
    stranger.makePart(spacex)
    movement = '4444333333324242424111111111111'    
    for moves in movement:
        for move in moves:
            stranger.move(spacex, str(move), 50)
    
    kate.makeDecoration(spacex, full=False)
    kate.openCurtain(spacex, openSpeed="fast", direct="close")
    
    print("works fine")

    
    
    

