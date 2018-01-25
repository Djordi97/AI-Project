from gameobjects import GameObject
from move import Move

class Agent:

    frontier = []
    closed = []
    current = (0,0)
    dict = {}
    currentDirection = None
    key = None

    def getSnakeHead(board):
        global initial
        for x in range(0,25):
            for y in range(0,25):
                if (board[x][y] == GameObject.SNAKE_HEAD):
                    initial = (x,y)
                    Agent.current = initial

    def getFood(board):
        global foodlist, food
        foodlist = []
        for x in range(0,25):
            for y in range(0,25):
                if (board[x][y] == GameObject.FOOD):
                    foodlist.append((x,y))
        shortdist = 10000
        for x in range(0,len(foodlist)):
            if(abs(foodlist[x][0]-initial[0])+abs(foodlist[x][1]-initial[1])<shortdist):
                shortdist = abs(foodlist[x][0]-initial[0])+abs(foodlist[x][1]-initial[1])
                food = (foodlist[x][0],foodlist[x][1])


    def validMove(x,y):
        if (x>=0 and x<25 and y>=0 and y<25):
            return True
        else:
            return False

    def determineMove(direction, moveToMake, position):
        global move
        xy_man = (moveToMake[0] - position[0], moveToMake[1] - position[1])
        if (direction.get_new_direction(Move.RIGHT).get_xy_manipulation() == xy_man):
            move = Move.RIGHT
        elif (direction.get_new_direction(Move.LEFT).get_xy_manipulation() == xy_man):
            move = Move.LEFT
        elif (direction.get_new_direction(Move.STRAIGHT).get_xy_manipulation() == xy_man):
            move = Move.STRAIGHT

    def setNewDirection():
        Agent.currentDirection = Agent.currentDirection.get_new_direction(move)
        Agent.current = best

    def mapPreviousPosition():
        for x in range(0,len(Agent.frontier)):
            if not(Agent.frontier[x] in Agent.dict):
                Agent.dict[Agent.frontier[x]] = Agent.current

    def extendFrontier(board):
        x = Agent.current[0]
        y = Agent.current[1]

        for i in range(0,len(list_man)):
            new_x = x+list_man[i][0]
            new_y = y+list_man[i][1]
            if (Agent.validMove(new_x,new_y)):
                if (((board[new_x][new_y] == GameObject.EMPTY) or
                    (board[new_x][new_y] ==GameObject.FOOD)) and
                    (new_x,new_y) not in (Agent.frontier) and
                    (new_x, new_y) not in (Agent.closed)):
                    Agent.frontier.append((new_x,new_y))

    def determineBestMove():
        global best
        cost = 100000
        Agent.closed.append(Agent.current)
        if (Agent.current in Agent.frontier):
            Agent.frontier.remove(Agent.current)
        for x in range(len(Agent.frontier)):
            g = abs(initial[0] - Agent.frontier[x][0]) + abs(initial[1] - Agent.frontier[x][1])
            h = abs(food[0] - Agent.frontier[x][0]) + abs(food[1] - Agent.frontier[x][1])
            if ((g+h)<cost):
                cost = g+h
                best = (Agent.frontier[x][0],Agent.frontier[x][1])

    def traceBack():
        Agent.key = food
        while not(Agent.dict[Agent.key] == initial):
            Agent.key = Agent.dict[Agent.key]

    def get_move(self, board, score, turns_alive, turns_to_starve, direction):
        global list_man, initialDirection
        print("start")
        print("score", score)
        initialDirection = direction
        Agent.currentDirection = direction
        #Get the position of the snake's head and the food object
        Agent.getSnakeHead(board)
        Agent.getFood(board)

        print("Start")

        while not(food in Agent.frontier):
            list_man = Agent.currentDirection.get_xy_moves()
        #In order to append the frontier with possible moves from the current posisiton of snake's head
            Agent.extendFrontier(board)
            Agent.mapPreviousPosition()
        #calculate the costs of possible moves according to A* Search
            Agent.determineBestMove()
            Agent.determineMove(Agent.currentDirection, best, Agent.current)
            Agent.setNewDirection()

        Agent.traceBack()
        Agent.determineMove(initialDirection, Agent.key, initial)
        Agent.frontier = []
        Agent.closed = []
        Agent.dict = {}

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
