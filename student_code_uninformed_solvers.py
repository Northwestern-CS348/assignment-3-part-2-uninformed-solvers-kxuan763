
from solver import *
from queue import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        if self.currentState.state == self.victoryCondition:
            return True

        # possible children
        if self.gm.getMovables():
            # initialize children
            for m in self.gm.getMovables():
                # explore child
                self.gm.makeMove(m)
                # fill in child fields
                child = GameState(self.gm.getGameState(), self.currentState.depth + 1, m)
                self.currentState.children.append(child)
                # link child to parent
                child.parent = self.currentState
                # come back to base node
                self.gm.reverseMove(m)

            for c in self.currentState.children:
                # if we find a new game state, go there
                if c not in self.visited:
                    # mark visited
                    self.visited[c] = True
                    # go
                    self.currentState = c
                    self.gm.makeMove(c.requiredMovable)
                    break
        # backtrack
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    q = Queue()
    moves = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        if self.currentState.state == self.victoryCondition:
            return True

        # Add all possible moves that can be taken from the given state to the states list of children
        # Iterate through all moves
        if self.gm.getMovables():
            # initialize children
            for m in self.gm.getMovables():
                # explore child
                self.gm.makeMove(m)
                # fill in child fields
                child = GameState(self.gm.getGameState(), 0, m)
                self.currentState.children.append(child)
                # link child to parent
                child.parent = self.currentState
                # come back to base node
                self.gm.reverseMove(m)

        # enqueue unvisited children
        for c in self.currentState.children:
            if c not in self.visited:
                self.q.put(c)

        # de-queue an unvisited state
        c = self.q.get()

        # construct path from current node to root
        rover = self.currentState
        home_path = []
        while rover.requiredMovable:
            home_path.append(rover.requiredMovable)
            rover = rover.parent

        # construct path from c to root (and flip it)
        rover = c
        child_path = []
        while rover.requiredMovable:
            child_path.append(rover.requiredMovable)
            rover = rover.parent
        child_path = reversed(child_path)

        # follow paths
        for s in home_path:
            self.gm.reverseMove(s)

        for s in child_path:
            self.gm.makeMove(s)

        # visit and mark
        self.currentState = c
        self.visited[c] = True
        self.moves +=1
        self.currentState.depth = self.moves

        return False
