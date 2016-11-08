from coordinate import Coordinate
from wall import Wall
import math
class Prey:
    def __init__(self,info):
        self.x_coord = info['prey'].x
        self.y_coord = info['prey'].y
        self.hunter_x = info['hunter'].x
        self.hunter_y = info['hunter'].y


    def move(self,info):
    	self.x_coord = info['prey'].x
        self.y_coord = info['prey'].y
        self.hunter_x = info['hunter'].x
        self.hunter_y = info['hunter'].y
        resp = {}
        resp['gameNum'] = info['gameNum']
        resp['tickNum'] = info['tickNum']
        if int(resp['tickNum']) % 2 == 0:
            resp['x'] = 0
            resp['y'] = 0
            return resp
        dist = math.pow(self.x_coord - self.hunter_x,2) + math.pow(self.y_coord -self.hunter_y ,2)
        if(dist>100):
            #100 because I am not taking sqaure root
            if(self.hunter_x > self.x_coord):
                resp['x'] = 1
            else:
                resp['x'] = -1
            if(self.hunter_y > self.y_coord):
                resp['y'] = 1
            else:
                resp['y'] = -1
            return resp
        else:
            if(self.x_coord < self.hunter_x):
                resp['x'] = - 1
            else:
                resp['x'] = 1
            if(self.y_coord < self.hunter_y):
                resp['y'] = 1 
            else:
                resp['y'] = - 1
            return resp

