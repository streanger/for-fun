import random
import numpy as np
import cv2
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def point_in_polygon(point, polygon_points):
    '''check if point is inside polygon'''
    status = random.choice([True, False])
    return status
    
    
def point_in_polygon_example(point=None, polygon_points=None):
    '''demonstrate how point in polygon case may look like'''
    
    if not point:
        # generate random point
        # point = (400, 400)
        point = (random.randrange(100, 700), random.randrange(100, 700))
    shapely_point = Point(*point)
    
    if not polygon_points:
        # generate four random points
        polygon_points = [(60, 60), (340, 40), (300, 360), (-60, 240)]
        
        
    polygon_points = [(x+240, y+200) for (x, y) in polygon_points]
    shapely_polygon = Polygon(polygon_points)
    polygon_points = np.array(polygon_points, np.int32)
    polygon_points = polygon_points.reshape((-1,1,2))
    
    
    # check if point is inside polygon
    # status = point_in_polygon(point, polygon_points)
    status = shapely_polygon.contains(shapely_point)
    
    
    # draw stuff
    color = (50, 50, 200)
    point_color = (50, 50, 200)
    if status:
        color = (50, 200, 50)
        point_color = (20, 150, 20)
        
    img = np.zeros((800, 800, 3), dtype = "uint8")
    cv2.polylines(img, [polygon_points], True, (100, 220, 100))
    cv2.line(img, point, point, point_color, 10)    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'point inside status: {}'.format(status), (30, 30),font, 0.8, color, 2, cv2.LINE_AA)
    
    
    # show in cv or whatever
    cv2.imshow('Window', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
if __name__ == "__main__":
    for x in range(100):
        point_in_polygon_example()
        
        
'''
todo:
    -implement alghoritm in pure python, without using externall libraries
    
'''
