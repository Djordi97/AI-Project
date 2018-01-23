from gameobjects import GameObject
from move import Move

class Agent:

    frontier = []
    closed = []

    def getSnakeHead(board):
        global current
        for x in range(0,25):
            for y in range(0,25):
                if (board[x][y] == GameObject.SNAKE_HEAD):
                    current = (x,y)

    def getFood(board):
        global food
        for x in range(0,25):
            for y in range(0,25):
                if (board[x][y] == GameObject.FOOD):
                    food = (x,y)

    def extendFrontier(board):
        if (board[current[0]+1][current[1]] == GameObject.EMPTY and (current[0]+1,current[1]) not in Agent.closed):
            Agent.frontier.append((current[0]+1,current[1],1))
        if(board[current[0]-1][current[1]] == GameObject.EMPTY and (current[0]-1,current[1]) not in Agent.closed):
            Agent.frontier.append((current[0]-1,current[1],1))
        if (board[current[0]][current[1]+1] == GameObject.EMPTY and (current[0],current[1]+1) not in Agent.closed):
            Agent.frontier.append((current[0],current[1]+1,1))
        if (board[current[0]][current[1]-1] == GameObject.EMPTY and (current[0],current[1]-1) not in Agent.closed):
            Agent.frontier.append((current[0],current[1]-1,1))
        print("current", current)
        print(Agent.frontier)

    def calculateCost():
        cost = 100000;
        best = (0,0);

        for x in range(len(Agent.frontier)):
            if ((Agent.frontier[x][2] + (food[0] - Agent.frontier[x][0]) + (food[1] - Agent.frontier[x][1]))<cost):
                cost = ((abs(food[0] - Agent.frontier[x][0])) + abs(food[1] - Agent.frontier[x][1]))
                best = (Agent.frontier[x][0],Agent.frontier[x][1])

    def get_move(self, board, score, turns_alive, turns_to_starve, direction):

        #Get the position of the snake's head and the food object
        Agent.getSnakeHead(board)
        Agent.getFood(board)

        #In order to append the frontier with possible moves from the current posisiton of snake's head
        Agent.extendFrontier(board)

        #calculate the costs of possible moves according to A* Search
        Agent.calculateCost()

        return Move.LEFT








        """This function behaves as the 'brain' of the snake. You only need to change the code in this function for
        the project. Every turn the agent needs to return a move. This move will be executed by the snake. If this
        functions fails to return a valid return (see return), the snake will die (as this confuses its tiny brain
        that much that it will explode). The starting direction of the snake will be North.

        :param board: A two dimensional array representing the current state of the board. The upper left most
        coordinate is equal to (0,0) and each coordinate (x,y) can be accessed by executing board[x][y]. At each
        coordinate a GameObject is present. This can be either GameObject.EMPTY (meaning there is nothing at the
        given coordinate), GameObject.FOOD (meaning there is food at the given coordinate), GameObject.WALL (meaning
        there is a wall at the given coordinate. TIP: do not run into them), GameObject.SNAKE_HEAD (meaning the head
        of the snake is located there) and GameObject.SNAKE_BODY (meaning there is a body part of the snake there.
        TIP: also, do not run into these). The snake will also die when it tries to escape the board (moving out of
        the boundaries of the array)

        :param score: The current score as an integer. Whenever the snake eats, the score will be increased by one.
        When the snake tragically dies (i.e. by running its head into a wall) the score will be reset. In ohter
        words, the score describes the score of the current (alive) worm.

        :param turns_alive: The number of turns (as integer) the current snake is alive.

        :param turns_to_starve: The number of turns left alive (as integer) if the snake does not eat. If this number
        reaches 1 and there is not eaten the next turn, the snake dies. If the value is equal to -1, then the option
        is not enabled and the snake can not starve.

        :param direction: The direction the snake is currently facing. This can be either Direction.NORTH,
        Direction.SOUTH, Direction.WEST, Direction.EAST. For instance, when the snake is facing east and a move
        straight is returned, the snake wil move one cell to the right.

        :return: The move of the snake. This can be either Move.LEFT (meaning going left), Move.STRAIGHT (meaning
        going straight ahead) and Move.RIGHT (meaning going right). The moves are made from the viewpoint of the
        snake. This means the snake keeps track of the direction it is facing (North, South, West and East).
        Move.LEFT and Move.RIGHT changes the direction of the snake. In example, if the snake is facing north and the
        move left is made, the snake will go one block to the left and change its direction to west.
        """

    def on_die(self):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.
        """
        pass
