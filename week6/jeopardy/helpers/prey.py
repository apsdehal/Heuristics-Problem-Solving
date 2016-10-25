from coordinate import Coordinate
from wall import Wall
class Prey:
    def __init__(self,info):
        self.x_coord = info['prey'].x
        self.y_coord = info['prey'].y
        self.hunter_x = info['hunter'].x
        self.hunter_y = info['hunter'].y


    def move(self,info):
        resp = {}
        resp['gameNum'] = info['gameNum']
        resp['tickNum'] = info['tickNum']

        if int(resp['tickNum']) % 2 == 0:
            resp['x'] = self.x_coord
            resp['y'] = self.y_coord
        else:
            dixt_x = abs(self.hunter_x - self.x_coord)
            dist_y = abs(self.hunter_y - self.y_coord)
            future_dist_x = abs(self.hunter_x + info['hunter'].vx - self.x_coord)
            future_dist_y = abs(self.hunter_y + info['hunter'].vy - self.y_coord)
            #if hunter is very near and moving closer then move perpendicular
            if(dixt_x <= 10 and dist_y <= 10 and future_dist_x < dixt_x and future_dist_y < dist_y):
                if(self.x_coord < self.hunter_x):
                    resp['x'] = self.x_coord - 1
                else:
                    resp['x'] = self.x_coord + 1
                if(self.y_coord < self.hunter_y):
                    resp['y'] = self.y_coord + 1 
                else:
                    resp['y'] = self.y_coord - 1
                return resp
            hitPoint = self.getHunterCollisionPoint(info)
            hitPointX = hitPoint.x
            hitPointY = hitPoint.y
            if(hitPointX - self.x_coord > 0):
                resp['x'] = self.x_coord - 1
            else:
                resp['x'] = self.x_coord + 1
            if(hitPointY - self.y_coord > 0):
                resp['y'] = self.y_coord - 1
            else:
                resp['y'] = self.y_coord + 1
                
        return resp

    def getHunterCollisionPoint(self,info):
        hunterX = info['hunter'].x
        hunterY = info['hunter'].y
        #TODO deep copy
        walls = info['walls']
        walls.append(Wall(Wall.HORIZONTAL, 0, 0 ,299))
        walls.append(Wall(Wall.HORIZONTAL, 299, 0 ,290))
        walls.append(Wall(Wall.VERTICAL, 0, 0 ,299))
        walls.append(Wall(Wall.VERTICAL, 299, 0 ,299))
        minDist = 10000
        hitPoint = None
        for wall in walls:
            if(wall.type == Wall.HORIZONTAL):
                #if hunter is going towards wall
                if(wall.coord - hunterY * info['hunter'].vy > 0):
                    dist = abs(wall.coord - hunterY)
                    hitPointX = hunterX + dist * info['hunter'].vx
                    hitPointY = wall.coord
                    if(hitPointX >= wall.start and hitPointX <= wall.end and dist < minDist):
                        minDist = dist
                        hitPoint = Coordinate(hitPointX,hitPointY)
            elif(wall.type == Wall.VERTICAL):
                if(wall.coord - hunterX * info['hunter'].vx > 0):
                    dist = abs(wall.coord - hunterX)
                    hitPointX = wall.coord
                    hitPointY = hunterY + dist * info['hunter'].vy
                    if(hitPointY >= wall.start and hitPointY <= wall.end and dist < minDist):
                        minDist = dist
                        hitPoint = Coordinate(hitPointX,hitPointY)
        return hitPoint
