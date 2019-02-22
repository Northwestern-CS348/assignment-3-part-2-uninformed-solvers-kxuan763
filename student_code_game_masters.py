from game_master import GameMaster
from read import *
from util import *


class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg1 = []
        peg2 = []
        peg3 = []

        ask1 = parse_input("fact: (on ?disk peg1")
        ask2 = parse_input("fact: (on ?disk peg2")
        ask3 = parse_input("fact: (on ?disk peg3")

        if self.kb.kb_ask(ask1):
            disks_on = self.kb.kb_ask(ask1).list_of_bindings
            for i in disks_on:
                disk = (int(i[0].bindings[0].constant.element[4]))
                peg1.append(disk)
        if self.kb.kb_ask(ask2):
            disks_on = self.kb.kb_ask(ask2).list_of_bindings
            for i in disks_on:
                disk = (int(i[0].bindings[0].constant.element[4]))
                peg2.append(disk)

        if self.kb.kb_ask(ask3):
            disks_on = self.kb.kb_ask(ask3).list_of_bindings
            for i in disks_on:
                disk = (int(i[0].bindings[0].constant.element[4]))
                peg3.append(disk)

        peg1 = tuple(sorted(peg1))
        peg2 = tuple(sorted(peg2))
        peg3 = tuple(sorted(peg3))

        return peg1, peg2, peg3

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        disk = movable_statement.terms[0]
        i_peg = movable_statement.terms[1]
        f_peg = movable_statement.terms[2]

        # all cases
        # retract old on and top
        old_peg = parse_input("fact: (on %s %s)" % (disk, i_peg))
        old_top = parse_input("fact: (top %s %s)" % (disk, i_peg))
        self.kb.kb_retract(old_peg)
        self.kb.kb_retract(old_top)

        # update secondary stack facts
        # cases:
        old_empty = parse_input("fact: (empty %s)" % f_peg)
        new_empty = parse_input("fact: (empty %s)" % i_peg)
        old_bottom = parse_input("fact: (bottom %s %s)" % (disk, i_peg))
        new_bottom = parse_input("fact: (bottom %s %s)" % (disk, f_peg))

        # if destination peg was empty
        if self.kb.kb_ask(old_empty):
            # it's not empty anymore
            self.kb.kb_retract(old_empty)
            # disk is now bottom
            self.kb.kb_assert(new_bottom)
        # it wasn't empty
        else:
            old_top_new = parse_input("fact: (top ?disk %s)" % f_peg)
            f_top = (self.kb.kb_ask(old_top_new).list_of_bindings[0])[0].bindings[0].constant.element
            # the top of the new peg isn't the top anymore
            self.kb.kb_retract(old_top_new)
            # the moving disk is now on top of that disk
            new_stack = parse_input("fact: (onTop %s %s)" % (disk, f_top))
            self.kb.kb_assert(new_stack)

        # if disk was bottom of initial peg
        if self.kb.kb_ask(old_bottom):
            # disk is no longer bottom
            self.kb.kb_retract(old_bottom)
            # initial peg is empty now
            self.kb.kb_assert(new_empty)
        # the disk was on top of another disk before
        else:
            old_stack = parse_input("fact: (onTop %s ?disk)" % disk)
            n_top = (self.kb.kb_ask(old_stack).list_of_bindings[0])[0].bindings[0].constant.element
            # it is no longer on top of that disk
            self.kb.kb_retract(old_stack)
            # that disk is now the top
            new_top_old = parse_input("fact: (top %s %s)" % (n_top, i_peg))
            self.kb.kb_assert(new_top_old)

        # assert new on and top
        new_peg = parse_input("fact: (on %s %s)" % (disk, f_peg))
        self.kb.kb_assert(new_peg)
        new_top = parse_input("fact: (top %s %s)" % (disk, f_peg))
        self.kb.kb_assert(new_top)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        row1 = ()
        row2 = ()
        row3 = ()

        ask1 = parse_input("fact: (location ?tile ?x 1")
        ask2 = parse_input("fact: (location ?tile ?x 2")
        ask3 = parse_input("fact: (location ?tile ?x 3")

        # tiles_in = self.kb.kb_ask(ask1).list_of_bindings
        for i in range(1, 4):
            ask = parse_input("fact: (location ?tile %s 1)" % str(i))
            disk = self.kb.kb_ask(ask)[0].bindings[0].constant.element[4]
            if disk == 'y':
                disk = -1,
            else:
                disk = int(disk),
            row1 = row1 + disk

        tiles_in = self.kb.kb_ask(ask2).list_of_bindings
        for i in range(1, 4):
            ask = parse_input("fact: (location ?tile %s 2)" % str(i))
            disk = self.kb.kb_ask(ask)[0].bindings[0].constant.element[4]
            if disk == 'y':
                disk = -1,
            else:
                disk = int(disk),
            row2 = row2 + disk

        tiles_in = self.kb.kb_ask(ask3).list_of_bindings
        for i in range(1, 4):
            ask = parse_input("fact: (location ?tile %s 3)" % str(i))
            disk = self.kb.kb_ask(ask)[0].bindings[0].constant.element[4]
            if disk == 'y':
                disk = -1,
            else:
                disk = int(disk),
            row3 = row3 + disk

        return row1, row2, row3

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        tile = movable_statement.terms[0]

        x_i = movable_statement.terms[1]
        y_i = movable_statement.terms[2]

        x_t = movable_statement.terms[3]
        y_t = movable_statement.terms[4]

        old_tile_xy = parse_input("fact: (location %s %s %s)" % (tile, x_i, y_i))
        new_tile_xy = parse_input("fact: (location %s %s %s)" % (tile, x_t, y_t))

        old_empty_xy = parse_input("fact: (location empty %s %s)" % (x_t, y_t))
        new_empty_xy = parse_input("fact: (location empty %s %s)" % (x_i, y_i))

        self.kb.kb_retract(old_tile_xy)
        self.kb.kb_retract(old_empty_xy)
        self.kb.kb_assert(new_empty_xy)
        self.kb.kb_assert(new_tile_xy)



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
