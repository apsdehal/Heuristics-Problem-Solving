from wall import Wall
from coordinate import Coordinate

def hunterNextMove(info):
	intersectingWallNumber = 0
	x = info['hunter'].x
	y = info['hunter'].y
	actual_x = apparent_x = x + info['hunter'].vx
	actual_y = apparent_y = y + info['hunter'].vy
	walls = info['walls']
	intersectingWalls = []
	for wall in walls:
		if(wall.type == Wall.HORIZONTAL):
			#handling case when wall is point sized
			if(apparent_y == wall.coord and apparent_x == wall.start and apparent_x==wall.end):
				#intersecting wall
				intersectingWallNumber += 1
				intersectingWalls.append(wall)
				actual_x = x
				actual_y = y
			#handling case when wall is not point sized
			elif(apparent_y == wall.coord and apparent_x >= wall.start and apparent_x<=wall.end):
				#intersecting wall
				intersectingWallNumber += 1
				intersectingWalls.append(wall)
				actual_y = apparent_y - info['hunter'].vy
		elif(wall.type == Wall.VERTICAL):
			#handling case when wall is point sized
			if(apparent_x == wall.coord and apparent_y == wall.start and apparent_y==wall.end):
				#intersecting wall
				intersectingWallNumber += 1
				intersectingWalls.append(wall)
				actual_x = x
				actual_y = y
			#handling case when wall is not point sized
			elif(apparent_x == wall.coord and apparent_y >= wall.start and apparent_y<=wall.end):
				#intersecting wall
				intersectingWallNumber += 1
				intersectingWalls.append(wall)
				actual_x = apparent_x - info['hunter'].vx

	if(intersectingWallNumber == 2):
		#wall1 is horizontal and wall2 is vertical
		if(intersectingWalls[0].type == Wall.HORIZONTAL):
			wall1 = intersectingWalls[0]
			wall2 = intersectingWalls[1]
		else:
			wall1 = intersectingWalls[1]
			wall2 = intersectingWalls[0]
		#when walls intersect
		if( (x > wall1.start and x < wall1.end) and not(y > wall2.start and y < wall2.end) ):
			#reflecting only from wall1
			actual_x = x + info['hunter'].vx
			actual_y = y
		elif( not(x > wall1.start and x < wall1.end) and (y > wall2.start and y < wall2.end) ):
			#reflecting only from wall2
			actual_x = x
			actual_y = y + info['hunter'].vy
		else:
			actual_x = x
			actual_y = y

	return actual_x,actual_y