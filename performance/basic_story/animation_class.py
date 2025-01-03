#this is takemyhand script
#font styles: normal, bold, roman, italic, underline, over, strike; combinations-> "bold italic"
#arc styles: "arc" "pieslice" "chord"
#skin color: #ffe6b3


#some sound would be usefull
from tkinter import *
import time
import random

class human:

    def __init__(self, name, sex):
        self.name = name
        self.sex = sex
        
    def makePart(self, spacex):
        if (self.sex == "male"):
            self.rightshoe = spacex.createShoes(vx=-1)
            self.leftshoe = spacex.createShoes(vx=1)
            self.rightleg = spacex.createLeg(vx=-1)
            self.leftleg = spacex.createLeg(vx=1)
            self.body = spacex.createBody()
            self.head = spacex.createHead()
            self.humanname = spacex.printName(self.name)    
        elif (self.sex == "female"):
            self.rightshoe = spacex.createShoes(vx=-1)
            self.leftshoe = spacex.createShoes(vx=1)
            self.rightleg = spacex.createLegF(vx=-1)
            self.leftleg = spacex.createLegF(vx=1)
            self.body = spacex.createBodyF()
            self.head = spacex.createHeadF()
            self.humanname = spacex.printName(self.name)
        else:
            print('what kind of monster is this?')    
        self.parts = [self.body,
                      self.head,
                      self.rightshoe,
                      self.leftshoe,
                      self.rightleg,
                      self.leftleg,
                      self.humanname]
                      
    def move(self, spacex, direction, steps):
        spacex.movePart(self.parts, direction, steps)    
    
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
    
    def openCurtain(self, spacex, openSpeed="normal", direct="open"):
        spacex.openCurtain(self.decoration, openSpeed, direct)
    
    
class myhand:
    
    def __init__(self):
        #make canvas
        self.screenWidth = 1366
        self.screenHeight = 768
        #self.screenWidth = 600
        #self.screenHeight = 400
        self.space = Tk()
        self.canvas = Canvas(self.space, width=self.screenWidth, height=self.screenHeight)
        self.canvas.config(bg="black")
        self.canvas.pack()
        
        #mirroring reverse
        self.vx, self.vy = 1, 1
        self.x, self.y = 1, 1
        #center of the view
        self.centerx, self.centery = 300, 225
        #person center; variable
        self.pcen = [120,120]
        #font atributes
        self.font = ('times', 12, 'bold')
        
    def setFont(self, family="times", fontsize=15, fontstyle='bold'):
        self.font = (family,fontsize,fontstyle)
    
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
        return self.canvas.create_text(self.pcen[0],self.pcen[1]-20, text=name, font=self.font, fill="white")
        
    def createLeg(self, vx=1,vy=1):
        self.vx = vx
        self.vy = vy
        manleg = self.canvas.create_polygon(self.pcen[0], self.pcen[1],
                                            self.pcen[0]-20*self.vx, self.pcen[1], 
                                            self.pcen[0]-10*self.vx, self.pcen[1]+70*self.vy, 
                                            self.pcen[0], self.pcen[1]+70*self.vy,  
                                            outline="white", fill="black", width=3)
        return manleg
        
    def createLegF(self, vx=1,vy=1):
        self.vx = vx
        self.vy = vy
        womanleg = self.canvas.create_polygon(self.pcen[0],self.pcen[1]+40,
                                              self.pcen[0]-13*self.vx,self.pcen[1]+40,
                                              self.pcen[0]-8*self.vx,self.pcen[1]+70*self.vy,
                                              self.pcen[0],self.pcen[1]+70*self.vy,
                                              outline="white",fill="#ffe6b3", width=2)
        return womanleg
    
    def createHead(self, vx=1, vy=1):
        self.vx = vx
        self.vy = vy
        head =  self.canvas.create_oval(self.pcen[0]-20,self.pcen[1]-100,self.pcen[0]+20,self.pcen[1]-60, outline="yellow", fill='#ffe6b3')
        return head
        
    def createHeadF(self, vx=1, vy=1):
        self.vx = vx
        self.vy = vy
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
        return self.canvas.create_polygon(self.pcen[0],self.pcen[1]+70,self.pcen[0]-10*self.vx,self.pcen[1]+70,self.pcen[0]-20*self.vx,self.pcen[1]+75,self.pcen[0]-20*self.vx,self.pcen[1]+80,self.pcen[0],self.pcen[1]+80,self.pcen[0],self.pcen[1]+80, outline="white", fill="black", width=3)

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
                                          outline="white", fill="black", width=3)
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
                                          outline="white", fill="black", width=3)
        skirt = self.canvas.create_polygon(self.pcen[0]-15,self.pcen[1]+10,
                                           self.pcen[0]-30,self.pcen[1]+45,
                                           self.pcen[0]+30,self.pcen[1]+45,
                                           self.pcen[0]+15,self.pcen[1]+10,
                                           outline="white", fill="black", width=3)
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
                                            fill="#b3ffff", width=1) 
        
        ground = self.canvas.create_polygon(0,self.screenHeight*0.9,
                                            self.screenWidth,self.screenHeight*0.9,
                                            self.screenWidth,self.screenHeight,
                                            0,self.screenHeight,
                                            fill="green", width=1)
        groundline = self.canvas.create_line(0,self.screenHeight*0.9,
                                            self.screenWidth,self.screenHeight*0.9,
                                            fill="brown", width=3)
                                            
        return groundline, ground, bluesky
        
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
                                              fill="black", width=5)                                    
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
                                              fill="black", width=5)                                    
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
    spacex = myhand()
    stranger = human("( ͡° ͜ʖ ͡°)", 'male')
    kate = human("kate", "female")
    kate.makeDecoration(spacex)
    kate.openCurtain(spacex, openSpeed="fast")
    
    stranger.setCenter(spacex, [100,200])
    stranger.makePart(spacex)
    movement = '4444333333324242424111111111111'    
    for moves in movement:
        for move in moves:
            stranger.move(spacex, str(move))
    
    kate.makeDecoration(spacex, full=False)
    kate.openCurtain(spacex, openSpeed="fast", direct="close")
    
    print("works fine")

    
    
    


