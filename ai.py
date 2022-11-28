import math
import pymunk
from pymunk import Vec2d
import gameobjects
from collections import defaultdict, deque
from gameobjects import *
# NOTE: use only 'map0' during development!

MIN_ANGLE_DIF = math.radians(3) # 3 degrees, a bit more than we can turn each tick



def angle_between_vectors(vec1, vec2):
    """ Since Vec2d operates in a cartesian coordinate space we have to
        convert the resulting vector to get the correct angle for our space.
    """
    vec = vec1 - vec2 
    vec = vec.perpendicular()
    return vec.angle

def periodic_difference_of_angles(angle1, angle2): 
    return  (angle1% (2*math.pi)) - (angle2% (2*math.pi))


class Ai:
    """ A simple ai that finds the shortest path to the target using 
    a breadth first search. Also capable of shooting other tanks and or wooden
    boxes. """

    def __init__(self, tank,  game_objects_list, tanks_list, space, currentmap,):
        self.tank               = tank
        self.game_objects_list  = game_objects_list
        self.tanks_list         = tanks_list
        self.space              = space
        self.currentmap         = currentmap
        self.flag = None
        self.MAX_X = currentmap.width - 1 
        self.MAX_Y = currentmap.height - 1

        self.path = deque()
        self.move_cycle = self.move_cycle_gen()
        self.update_grid_pos()

    def update_grid_pos(self):
        """ This should only be called in the beginning, or at the end of a move_cycle. """
        self.grid_pos = self.get_tile_of_position(self.tank.body.position)

    def decide(self):
        """ Main decision function that gets called on every tick of the game. """
<<<<<<< HEAD
        next(self.move_cycle)

=======
        self.update_grid_pos()
        self.find_shortest_path(0)
        self.maybe_shoot()
        next(self.move_cycle)
        pass # To be implemented
>>>>>>> 6c34a84da6b6505610542e40fee4f742ea560404

    def maybe_shoot(self):
        """ Makes a raycast query in front of the tank. If another tank
            or a wooden box is found, then we shoot. 
        """
<<<<<<< HEAD

        pass # To be implemented
=======
        tank_angle = self.tank.body.angel + math.pi/2
        pos = Vec2d(self.tank.body.position)

        start_coordinate = pos + (0.55 * math.cos(tank_angle), 0.55 * math.sin(tank_angle)) 
        end_coordinate = pos + (69 * math.cos(tank_angle), 69 * math.sin(tank_angle)) #69 is big enough
        self.space.segment_query_first
        obj = self.space.segment_query_first(start_coordinate,end_coordinate,0,pymunk.ShapeFilter())
        if hasattr(obj, 'shape'):
            if hasattr(obj.shape.parent, 'parent'):
                if isinstance(obj,gameobjects.Box) and obj.shape.parent.destructable:
                    box = obj.shape.parent
                    self.tank.shoot()

                elif isinstance(obj.shape.tank,  GameObject.tank):
                    self.tank.shoot()

         # Probably done, maybe needs tweaking-Valle
>>>>>>> 6c34a84da6b6505610542e40fee4f742ea560404

    def move_cycle_gen (self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """ 
        while True:
<<<<<<< HEAD
            shorest_path = self.find_shortest_path()
            next_coord = shorest_path.popleft()
            if len(shorest_path) == 0:
                yield
                continue
            yield
            needed_angle = angle_between_vectors(self.tank.body.position, next_coord + Vec2d(0.5, 0.5))
            p_angle = periodic_difference_of_angles(self.tank.body.angle, needed_angle)
            if p_angle < -math.pi:
                self.tank.turn_left()
                yield
            elif 0 > p_angle > math.pi:
                self.tank.turn_right()
                yield
            else:
                self.tank.turn_right()
                yield

            while abs(p_angle) >= MIN_ANGLE_DIF:
                p_angle = periodic_difference_of_angles(self.tank.body.angle, needed_angle)
                yield

            self.tank.stop_turning()
            distance = self.tank.body.position.get_distance(next_coord + Vec2d(0.5, 0.5))
            self.tank.accelerate()
            while distance > 0.25:
                distance = self.tank.body.position.get_distance(next_coord + Vec2d(0.5, 0.5))
                yield
            if self.flag == True:
                self.tank.stop_moving()
            yield



    def find_shortest_path(self):
        """ A simple Breadth First Search using integer coordinates as our nodes.
            Edges are calculated as we go, using an external function.
        """
        shortest_path = []
        start = self.grid_pos
        bfs_queue = deque()
        bfs_queue.append(start)
        explored = set(start.int_tuple)
        theory_pos_tree = {}  

        while len(bfs_queue) > 0:
            theory_pos = bfs_queue.popleft()
            if theory_pos == self.get_target_tile(): # if we found the flag
                while theory_pos != start:
                    shortest_path.append(theory_pos)
                    parent = theory_pos_tree[theory_pos.int_tuple]
                    theory_pos = parent
                shortest_path.reverse()
                break
            for neighbour in self.get_tile_neighbors(theory_pos):
                if neighbour.int_tuple not in explored:
                    bfs_queue.appendleft(neighbour)
                    theory_pos_tree[neighbour.int_tuple] = theory_pos
                    explored.add(neighbour.int_tuple)
    
=======
            self.update_grid_pos()
            findso
        
    def find_shortest_path(self, b):
        """ A simple Breadth First Search using integer coordinates as our nodes.
            Edges are calculated as we go, using an external function.
        """
        bfs_queue = deque()

        # To be implemented
        while len(bfs_queue) > 0:
        if b < 10:
            b += 1
            shortest_path = []
            a = self.get_tile_neighbors(self.grid_pos)
            return self.find_shortest_path(b)
>>>>>>> 6c34a84da6b6505610542e40fee4f742ea560404
        return deque(shortest_path)

            
    def get_target_tile(self):
        """ Returns position of the flag if we don't have it. If we do have the flag,
            return the position of our home base.
        """
        if self.tank.flag is not None:
            x, y = self.tank.start_position
        else:
            self.get_flag() # Ensure that we have initialized it.
            x, y = self.flag.x, self.flag.y
        return Vec2d(int(x), int(y))

    def get_flag(self):
        """ This has to be called to get the flag, since we don't know
            where it is when the Ai object is initialized.
        """
        if self.flag is None:
            # Find the flag in the game objects list
            for obj in self.game_objects_list:
                if isinstance(obj, gameobjects.Flag):
                    self.flag = obj
                    break
        return self.flag


    def get_tile_of_position(self, position_vector):
        """ Converts and returns the float position of our tank to an integer position. """
        x, y = position_vector
        return Vec2d(int(x), int(y))

    def get_tile_neighbors(self, coord_vec):
        """ Returns all bordering grid squares of the input coordinate.
            A bordering square is only considered accessible if it is grass
            or a wooden box.
        """
        neighbors = [] # Find the coordinates of the tiles' four neighbors
        filtered_neighboors = []
        coord = self.get_tile_of_position(coord_vec)
        neighbors.append(coord + Vec2d(1,0))
        neighbors.append(coord + Vec2d(-1,0))
        neighbors.append(coord + Vec2d(0,-1))
        neighbors.append(coord + Vec2d(0,1))
        for i in range(4):
            if self.filter_tile_neighbors(neighbors[i]) == True:
                filtered_neighboors.append(neighbors[i])
        return filtered_neighboors

    def filter_tile_neighbors (self, coord):
        tile = self.get_tile_of_position(coord)

        if coord[0] > self.MAX_X or coord[1] > self.MAX_Y or coord[0] <= 0 or coord[1] <= 0:
                return False
        if self.currentmap.boxAt(tile[0],tile[1]) == 0:
            return True
        else:
            return False

SimpleAi = Ai # Legacy