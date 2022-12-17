import math
import pymunk
from pymunk import Vec2d
import gameobjects
from collections import defaultdict, deque
from gameobjects import *
import maps

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
    STAT_INCREASE = 1.3
    def __init__(self, tank,  game_objects_list, tanks_list, space, currentmap, unfair_ai, bullet_list):
        self.tank               = tank
        self.game_objects_list  = game_objects_list
        self.tanks_list         = tanks_list
        self.space              = space
        self.currentmap         = currentmap
        self.flag = None
        self.bullet_list        = bullet_list
        self.MAX_X = currentmap.width - 1 
        self.MAX_Y = currentmap.height - 1
        self.path = deque()
        self.move_cycle = self.move_cycle_gen()
        self.update_grid_pos()
        if self.currentmap == maps.map1 or self.currentmap == maps.map2: 
            self.metal_box = True
        else:
            self.metal_box = False
        if unfair_ai == True:
            self.tank.stat_increase(Ai.STAT_INCREASE)
    def update_grid_pos(self):
        """ This should only be called in the beginning, or at the end of a move_cycle. """
        self.grid_pos = self.get_tile_of_position(self.tank.body.position)

    def decide(self):
        """ Main decision function that gets called on every tick of the game. 
            TODO: Make the ai realize it died and reset self.move_cycle
        """
        self.update_grid_pos()
        next(self.move_cycle)
        if self.tank.cooldown_tracker >= 60:
            self.maybe_shoot()

    def ai_respawn(self):
        inst_ai = Ai(self.tank, self.game_objects_list, self.tanks_list, self.space, self.currentmap, self.bullet_list)
        del self
        return inst_ai
    def maybe_shoot(self):
        """ Makes a raycast query in front of the tank. If another tank
            or a wooden box is found, then we shoot. 
        """

        tank_angle = self.tank.body.angle + math.pi/2
        pos = Vec2d(self.tank.body.position)

        start_coordinate = pos + (0.55 * math.cos(tank_angle), 0.55 * math.sin(tank_angle)) 
        end_coordinate = pos + (69 * math.cos(tank_angle), 69 * math.sin(tank_angle)) #69 is big enough
        self.space.segment_query_first
        obj = self.space.segment_query_first(start_coordinate,end_coordinate,0,pymunk.ShapeFilter())
        if hasattr(obj, 'shape'):
            if hasattr(obj.shape, 'parent'):
                if isinstance(obj.shape.parent, Tank):
                    self.bullet_list.append(self.tank.shoot(self.space))
                elif isinstance(obj.shape.parent, Box) and obj.shape.parent.destructable == True:
                    self.bullet_list.append(self.tank.shoot(self.space))


    def move_cycle_gen (self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """ 
    
        while True: #Something like as long as nextcoord is within 2 moves from our body otherwise reset or something like that. 
            self.update_grid_pos()
            shortest_path = self.find_shortest_path()
            if len(shortest_path) == 0:
                yield
                continue
            yield
            next_coord = shortest_path.popleft()
            needed_angle = angle_between_vectors(self.tank.body.position, next_coord + Vec2d(0.5, 0.5))
            p_angle = periodic_difference_of_angles(self.tank.body.angle, needed_angle)

            if p_angle < -math.pi:
                self.tank.turn_left()
                yield
            elif p_angle > math.pi:
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
            while distance > 0.3:
                distance_check = pygame.math.Vector2(next_coord).distance_to(pygame.math.Vector2(self.grid_pos))
                if distance_check >= 1.5:
                    self.move_cycle = self.move_cycle_gen()
                distance = self.tank.body.position.get_distance(next_coord + Vec2d(0.5, 0.5))
                yield
            self.tank.stop_moving()
            yield
    def has_moved(self, last_location, next_location):
        # Calculate the distance between the last location and the next location
        distance = pygame.math.Vector2(next_location).distance_to(pygame.math.Vector2(last_location))
        return distance > 0
    def find_shortest_path(self):
        """ A simple Breadth First Search using integer coordinates as our nodes.
            Edges are calculated as we go, using an external function.
        """
        shortest_path = []
        paths = {self.grid_pos.int_tuple: [self.grid_pos]}
        queue = deque()
        visited = set()
        visited.add(self.grid_pos.int_tuple)
        queue.append(self.grid_pos)

        while queue:
            node = queue.popleft()
            if node == self.get_target_tile():
                shortest_path = deque(paths[node.int_tuple])
                shortest_path.popleft()
                break
            for neighbor in self.get_tile_neighbors(node):
                next_node = neighbor.int_tuple
                if next_node not in visited: 
                    queue.append(neighbor)
                    visited.add(next_node)
                    temp_list = paths[node.int_tuple].copy()
                    paths[next_node] = temp_list
                    paths[next_node].append(neighbor)

        return shortest_path


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
        coord = self.get_tile_of_position(coord_vec)
        neighbors.append(coord + Vec2d(1,0))
        neighbors.append(coord + Vec2d(-1,0))
        neighbors.append(coord + Vec2d(0,-1))
        neighbors.append(coord + Vec2d(0,1))
        return(filter(self.filter_tile_neighbors, neighbors))
        

    def filter_tile_neighbors (self, coord):

        if coord[0] > self.MAX_X or coord[1] > self.MAX_Y or coord[0] < 0 or coord[1] < 0:
            return False
        if self.metal_box == True:
            if self.currentmap.boxAt(coord[0],coord[1]) == 3 or self.currentmap.boxAt(coord[0],coord[1]) == 0 or self.currentmap.boxAt(coord[0],coord[1]) == 2:
                return True
            else:
                return False
        if self.currentmap.boxAt(coord[0],coord[1]) == 1 or self.currentmap.boxAt(coord[0],coord[1]) == 2 or self.currentmap.boxAt(coord[0],coord[1]) == 3:
            return False
        return True

SimpleAi = Ai # Legacy
