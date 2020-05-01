import random
from ship import Ship
from board import Board
from position import Position


# This is a naive implementation of a Player class that:
# 1. Sets up the same board every time (i.e. a static layout)
# 2. Fires randomly, without remembering which shots were hits and misses
class Player:

    # Each player has a name. There should be no need to change or delete this!
    def __init__(self, name):
        self.__name = name
        self.results = []
        # all position
        self.hitpos = []
        # hit position
        self.hitonpos = []


    def get_name(self):
        return self.__name

    def __str__(self):
        return self.get_name()

    # get_board should return a Board object containing 5 ships:
    # 1 aircraft carrier (length = 5)
    # 1 battleship (length = 4)
    # 1 cruiser (length = 3)
    # 1 submarine (length = 3)
    # 1 destroyer (length = 2)
    # You can make your own fun names for the ships, but the number and lengths
    # of the ship will be validated by the framework. Printing the board will
    # show the first letter of each ship's name.

    # This implementation returns the first sample layout from this web page:
    # http://datagenetics.com/blog/december32011/index.html
    def get_board(self):
        ships_1 = [Ship('Carrier', Position('J', 2), 5, False),
                   Ship('battleship', Position('E', 5), 4, True),
                   Ship('submarine', Position('B', 2), 3, False),
                   Ship('crusier', Position('D', 8), 3, False),
                   Ship('destroyer', Position('E', 3), 2, True)]
        ships_2 = [Ship('Carrier', Position('D', 2), 5, False),
                   Ship('battleship', Position('F', 5), 4, True),
                   Ship('submarine', Position('A', 2), 3, False),
                   Ship('crusier', Position('A', 9), 3, True),
                   Ship('destroyer', Position('I', 3), 2, True)]
        ships_3 = [Ship('Carrier', Position('C', 1), 5, True),
                   Ship('battleship', Position('F', 7), 4, True),
                   Ship('submarine', Position('A', 2), 3, False),
                   Ship('crusier', Position('C', 9), 3, True),
                   Ship('destroyer', Position('H', 4), 2, True)]
        ships_list = [ships_1, ships_2, ships_3]
        return Board(ships_list[random.randint(0, 2)])

    # random shot
    def select_random_shot(self):
        row = chr(64 + random.randint(1, 10))
        if row == 'A' or row == 'C' or row == 'E' or row == 'G' or row == 'I':
            col = random.choice((1, 3, 5, 7, 9))
        else:
            col = random.choice((2, 4, 6, 8, 10))
        return Position(row, col)

    def random_shot(self):
        shot = self.select_random_shot()
        shot_pos = (chr(shot.get_row_idx()+65), shot.get_col_idx()+1)
        while shot_pos in self.hitpos:
            shot = self.select_random_shot()
            shot_pos = (chr(shot.get_row_idx()+65), shot.get_col_idx()+1)
        self.hitpos.append(shot_pos)
        return shot

    # target shot
    def clear_around(self):
        hit_or_not = self.results[-1]
        pos = hit_or_not[0]
#        row = hit_or_not[0].get_row_idx() + 65
#        col = hit_or_not[0].get_col_idx() + 1
#        shot = Position(row, col)
        pos_loc = (chr(pos.get_row_idx()+65), pos.get_col_idx()+1)
        self.hitpos.append(pos_loc)
        if hit_or_not[1] is True:
            shot_list = self.target_around(pos)
            for x in shot_list:
                if (chr(x.get_row_idx()+65), x.get_col_idx()+1) not in set(self.hitonpos + self.hitpos):
                    self.hitonpos.append((chr(x.get_row_idx()+65), x.get_col_idx()+1))
                    self.hitpos.append((chr(x.get_row_idx()+65), x.get_col_idx()+1))

#            for shot in self.hitonpos:
#                if shot in self.hitpos:
#                    self.hitonpos.remove(shot)
#           print(hit_or_not[0])

    def target_shot(self):
        pos = self.hitonpos.pop()
        return Position(pos[0], pos[1])

    def target_around(self, pos):
        target = []
        row = pos.get_row_idx() + 65
        col = pos.get_col_idx() + 1

        N = Position(chr(row - 1), col)
        if N.validate() is True:
            target.append(N)

        S = Position(chr(row + 1), col)
        if S.validate() is True:
            target.append(S)

        E = Position(chr(row), (col + 1))
        if E.validate() is True:
            target.append(E)

        W = Position(chr(row), (col - 1))
        if W.validate() is True:
            target.append(W)
 
        return target

    def next_shot(self):
        # 1st
#        self.hit()
        if len(self.results) == 0:
#            print('-----')
            return self.random_shot()
        else:
            self.clear_around()
            if len(self.hitonpos) > 0:
                return self.target_shot()
            else:
    #            print(self.hitonpos)
                return self.random_shot()
    # result is a tuple consisting of:
    # - the shot location (a Position object)
    # - whether the shot was a hit (True) or a miss (False)
    # - whether a ship was sunk (True) or not (False)

    def post_shot_result(self, result):
        self.results.append(result)