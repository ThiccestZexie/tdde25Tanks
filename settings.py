import maps

class Settings:
    def __init__(self):
        self.hot_seat_multiplayer = False
        self.current_map = maps.map0
        self.fog_of_war = False
        self.unfair_ai = True
        self.wincon = 0 # 0 = time based | 1 = total amount of rounds | 2 = score based 

        # win con variabels
        self.time = 120
        self.t_rounds = 10
        self.points_to_win = 3
