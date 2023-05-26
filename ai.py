import math
import pymunk
from pymunk import Vec2d
import gameobjects
from collections import defaultdict, deque
from gameobjects import *
import maps

# NOTE: use only 'map0' during development!

MIN_ANGLE_DIF = math.radians(5) # 3 degrees, a bit more than we can turn each tick

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
    STAT_INCREASE = 5
    def __init__(self, tank,  game_objects_list, tanks_list, space, currentmap, unfair_ai, bullet_list):
        self.tank               = tank
        self.game_objects_list  = game_objects_list
        self.tanks_list         = tanks_list
        self.space              = space
        self.currentmap         = currentmap
        self.flag = None
        self.timer = 0
        self.bullet_list        = bullet_list
        self.grid_pos = self.get_tile_of_position(self.tank.body.position)
        self.MAX_X = currentmap.width - 1 
        self.MAX_Y = currentmap.height - 1
        self.path = deque()
        self.move_cycle = self.move_cycle_gen()
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
        """Main decision function that gets called on every tick of the game.
        Resets the AI if it keeps moving in the same direction without progress.
        """
        next(self.move_cycle)
        if self.tank.cooldown_tracker >= 60:
            self.maybe_shoot()

        # Check if the AI is not making progress (e.g., driving into a wall)
        current_tile = self.get_tile_of_position(self.tank.body.position)
        if  self.is_stuck() and current_tile == self.grid_pos:
            self.reset_ai()
            self.timer = 0
    def is_stuck(self):
        """Check if the AI is stuck by comparing the current direction with the previous direction."""
        if len(self.path) >= 2:
            current_direction = self.path[1] - self.path[0]
            previous_direction = self.grid_pos - self.path[0]
            return current_direction == previous_direction
        return False

    def reset_ai(self):
        """Reset the AI's move_cycle and path attributes."""
        self.update_grid_pos()
        self.path = deque()
        self.move_cycle = self.move_cycle_gen()

    def ai_respawn(self):
        self.tank.respawn(self.flag)
        self.path = deque()
        self.update_grid_pos()
    def maybe_shoot(self):
        """ Makes a raycast query in front of the tank. If another tank
            or a wooden box is found, then we shoot. 
        """

        tank_angle = self.tank.body.angle + math.pi/2
        pos = Vec2d(self.tank.body.position)

        start_coordinate = pos + (0.55 * math.cos(tank_angle), 0.55 * math.sin(tank_angle)) 
        end_coordinate = pos + (65 * math.cos(tank_angle), 65 * math.sin(tank_angle)) #65 is big enough
        self.space.segment_query_first
        obj = self.space.segment_query_first(start_coordinate,end_coordinate,0,pymunk.ShapeFilter())
        if hasattr(obj, 'shape'):
            if hasattr(obj.shape, 'parent'):
                if isinstance(obj.shape.parent, Tank):
                    self.bullet_list.append(self.tank.shoot(self.space))
                elif isinstance(obj.shape.parent, Box) and obj.shape.parent.destructable == True:
                    self.bullet_list.append(self.tank.shoot(self.space))


    def move_cycle_gen(self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """
        while True:
            self.update_grid_pos()
            self.path = self.find_shortest_path()
            if len(self.path) <= 0:
                self.allow_metalbox = True
                yield
                continue

            self.allow_metalbox = False
            next_coord = self.path.popleft()
            print(self.tank.name, " ", self.path)
            yield
            target_angle = angle_between_vectors(self.tank.body.position, next_coord + Vec2d(0.5, 0.5))
            p_angle = periodic_difference_of_angles(self.tank.body.angle, target_angle)

            if p_angle < -math.pi:
                self.tank.turn_left()
                yield
            elif 0 > p_angle > -math.pi:
                self.tank.turn_right()
                yield
            elif math.pi > p_angle > 0:
                self.tank.turn_left()
                yield
            else:
                self.tank.turn_right()
                yield

            while abs(p_angle) >= MIN_ANGLE_DIF:
                p_angle = periodic_difference_of_angles(self.tank.body.angle, target_angle)
                yield

            self.tank.stop_turning()
            self.tank.accelerate()
            distance = self.tank.body.position.get_distance(next_coord + Vec2d(0.5, 0.5))
            while distance > 0.3:
                distance = self.tank.body.position.get_distance(next_coord + Vec2d(0.5, 0.5))
                yield
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
        visited_nodes = set(start.int_tuple)
        node_tree = {}

        while len(bfs_queue) > 0:
            node = bfs_queue.popleft()
            if node == self.get_target_tile():
                while node != start:
                    shortest_path.append(node)
                    parent = node_tree[node.int_tuple]
                    node = parent
                shortest_path.reverse()
                break
            for neighbour in self.get_tile_neighbors(node):
                if neighbour.int_tuple not in visited_nodes:
                    bfs_queue.append(neighbour)
                    node_tree[neighbour.int_tuple] = node
                    visited_nodes.add(neighbour.int_tuple)

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
        coord = self.get_tile_of_position(coord_vec)
        neighbors.append(coord + Vec2d(-1,0))
        neighbors.append(coord + Vec2d(1,0))
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
        if self.currentmap.boxAt(coord[0],coord[1]) == 1 or self.currentmap.boxAt(coord[0],coord[1]) == 3:
            return False
        return True

SimpleAi = Ai # Legacy
