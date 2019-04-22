import sys
import os
import numpy as np
import cv2


def script_path():
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def draw_planet(img, center, radius, color, name, key):
    # center of ellipse, distance, color, name
    radius = round(radius)
    long_axis = round(radius)
    short_axis = round(long_axis/3)
    cv2.ellipse(img, center, (long_axis, short_axis), 0, 0, 360, color, 2)
    cv2.circle(img, (center[0] - radius, center[1]), 8, (255, 255, 255), -1)     # draw planet
    cv2.circle(img, (center[0] - radius, center[1]), 5, color, -1)     # draw planet
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, name, (center[0] - radius - key*20, center[1] - key*50), font, 3, color, 2, cv2.LINE_AA)
    return img
    
    
def planets_parameters():
    planets = {
        'Mercury' : (57.740, (50,50,255)),
        'Venus' : (108.141, (250,250,155)),
        'Earth' : (149.504, (250,200,105)),
        'Mars' : (227.798, (50,50,255)),
        'Jupiter' : (777.840, (150, 50, 155)),
        'Saturn' : (1426.100, (250,250,155)),
        'Uranus' : (2867.830, (250,250,155)),
        'Neptune' : (4493.650, (250,250,155)),
    }
    return planets
    
def show_image(title, image):
    '''
    WINDOW_AUTOSIZE
    WINDOW_FREERATIO
    WINDOW_FULLSCREEN
    WINDOW_GUI_EXPANDED
    WINDOW_GUI_NORMAL
    WINDOW_KEEPRATIO
    WINDOW_NORMAL
    WINDOW_OPENGL
    '''
    cv2.namedWindow(title, cv2.WINDOW_FREERATIO)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
if __name__ == "__main__":
    script_path()
    height, width = (4000, 10000)
    img = np.zeros((height,width,3), np.uint8)
    center = tuple(map(int, (width/2, height/2)))
    cv2.circle(img, center, 15, (100, 255, 255), -1)     # sun position
    
    # draw planets
    planets = planets_parameters()
    for key, planet in enumerate(planets.keys()):
        radius, color = planets[planet]
        print("{} -> {} -> {}".format(planet, radius, color))
        img = draw_planet(img, center, radius, color, planet, key)
    
    show_image('img', img)
    cv2.imwrite('solar_system.png', img)
    
    
    
    
    
    
    
    
    