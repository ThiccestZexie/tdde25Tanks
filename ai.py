import math
import pymunk
from pymunk import Vec2d
import gameobjects
from gameobjects import Tank, Box
from collections import defaultdict, deque

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

    def __init__(self, tank,  game_objects_list, tanks_list, space, currentmap):
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

        self.allow_metal = False

    def update_grid_pos(self):
        """ This should only be called in the beginning, or at the end of a move_cycle. """
        self.grid_pos = self.get_tile_of_position(self.tank.body.position)

    def decide(self):
        """ Main decision function that gets called on every tick of the game. """
        if self.tank.shoot_cooldown < 1:
            self.maybe_shoot()

        next(self.move_cycle)

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
                    self.game_objects_list.append(self.tank.shoot(self.space))
                elif isinstance(obj.shape.parent, Box) and obj.shape.parent.destructable == True:
                    self.game_objects_list.append(self.tank.shoot(self.space))


    def move_cycle_gen (self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """ 
        while True:
            
            self.update_grid_pos()
            next_coord = self.get_next_centered_coord(self.grid_pos)
            yield

            # Adjust angle
            if abs(self.get_angle_difference(next_coord)) > math.pi/10:
                while (abs(angle_difference
                           := self.get_angle_difference(next_coord))
                       > MIN_ANGLE_DIF):

                    self.tank.stop_moving()

                    if (0 <= angle_difference <= math.pi):
                        self.tank.turn_left()
                    elif (math.pi <= angle_difference <= 2 * math.pi):
                        self.tank.turn_right()
                    else:
                        self.tank.turn_right()

                    yield

                self.tank.stop_turning()
                yield

            # Adjust position
            distance = self.tank.body.position.get_distance(next_coord)
            previous, current = distance, distance
            while previous >= current and current > 0.1:
                self.tank.accelerate()
                previous = current
                current = self.tank.body.position.get_distance(next_coord)

                # Check for respawn or stuck AI.
                if current > 2:
                    break
                yield

    def get_angle_difference(self, target_coord):
        """
        Return position that the tank should face to get to the target.

        Returns periodic difference between the tank angle and the angle of the
        difference vector between the tank position and the target position.
        """
        return periodic_difference_of_angles(
                self.tank.body.angle,
                angle_between_vectors(
                    self.tank.body.position,
                    target_coord)
                )
    def find_shortest_path(self):
        """ A simple Breadth First Search using integer coordinates as our nodes.
            Edges are calculated as we go, using an external function.
        """
        # To be implemented


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
    def get_next_centered_coord(self, coord: Vec2d) -> Vec2d:
        """Return a centered vector on the next coordinate."""
        if not self.path or coord not in self.get_tile_neighbors(coord):
            self.path = self.find_shortest_path()

        return self.path.popleft() + Vec2d(0.5, 0.5)
            
    def get_target_tile(self):
        """ Returns position of the flag if we don't have it. If we do have the flag,
            return the position of our home base.
        """
        if self.tank.flag != None:
            x, y = self.tank.start_position
        else:
            self.flag = self.get_flag() # Ensure that we have initialized it.
            x, y = self.flag.x, self.flag.y
        return Vec2d(int(x), int(y))

    def get_flag(self):
        """ This has to be called to get the flag, since we don't know
            where it is when the Ai object is initialized.
        """
        if self.flag == None:
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
        if self.allow_metal == True:
            if self.currentmap.boxAt(coord[0],coord[1]) == 3 or self.currentmap.boxAt(coord[0],coord[1]) == 0 or self.currentmap.boxAt(coord[0],coord[1]) == 2:
                return True
            else:
                return False
        if self.currentmap.boxAt(coord[0],coord[1]) == 1 or self.currentmap.boxAt(coord[0],coord[1]) == 3:
            return False
        return True



SimpleAi = Ai # Legacy