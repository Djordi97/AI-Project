from gameobjects import GameObject
from move import Move
from math import *
import time

class Agent:

    board_width = 40
    board_height = 40
    timerStarted = False
    frontier = None
    closed = None
    current = None
    dict = None
    costDict = None
    currentDirection = None
    key = None
    timeList = []

    def getSnakeHead(board):
        global initial
        for x in range(0,Agent.board_width):
            for y in range(0,Agent.board_height):
                if (board[x][y] == GameObject.SNAKE_HEAD):
                    initial = (x,y)
                    Agent.current = initial

    def getFood(board):
        global foodlist, food
        foodlist = []
        for x in range(0,Agent.board_width):
            for y in range(0,Agent.board_height):
                if (board[x][y] == GameObject.FOOD):
                    foodlist.append((x,y))
        shortdist = 10000
        for x in range(0,len(foodlist)):
            if(abs(foodlist[x][0]-initial[0])+abs(foodlist[x][1]-initial[1])<shortdist):
                shortdist = abs(foodlist[x][0]-initial[0])+abs(foodlist[x][1]-initial[1])
                food = (foodlist[x][0],foodlist[x][1])

    def findBodyParts(board):
        global body_parts
        body_parts = []
        for x in range(0,Agent.board_width):
            for y in range(0,Agent.board_height):
                if (board[x][y] == GameObject.SNAKE_BODY):
                    body_parts.append((x,y))

    def validMove(x,y):
        return (x>=0 and x<Agent.board_width and y>=0 and y<Agent.board_height)


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

    def scanArea(tuple,board):
        global foodClose, bodyClose
        foodClose = False
        bodyClose = False
        x = tuple[0]
        y = tuple[1]
        for i in range(0, len(list_man)):
            new_x = x+list_man[i][0]
            new_y = y+list_man[i][1]
            if((new_x,new_y) in body_parts):
                bodyClose = True
            if((new_x,new_y) in foodlist):
                foodClose = True

    def extendFrontier(board):
        x = Agent.current[0]
        y = Agent.current[1]
        for i in range(0, len(list_man)):
            new_x = x+list_man[i][0]
            new_y = y+list_man[i][1]
            if(Agent.validMove(new_x, new_y)):
                if((new_x, new_y) not in Agent.frontier and
                   (new_x, new_y) not in Agent.closed):
                   if((board[new_x][new_y] == GameObject.EMPTY) or
                             (board[new_x][new_y] == GameObject.FOOD)):
                             Agent.frontier.append((new_x,new_y))

                 #  if(firstTime == True):
                #   elif(firstTime == False):
                        #if(not (board[new_x][new_y] == GameObject.WALL)):
                            #Agent.frontier.append((new_x,new_y))

    def determineBestMove(board,score):
        global best
        cost = 100000
        changes = 0
        Agent.closed.append(Agent.current)
        if (Agent.current in Agent.frontier):
            Agent.frontier.remove(Agent.current)
        for x in range(len(Agent.frontier)):
            #g = sqrt(pow((initial[0] - Agent.frontier[x][0]),2) + pow((initial[1] - Agent.frontier[x][1]),2))
            g = abs(initial[0] - Agent.frontier[x][0]) + abs(initial[1] - Agent.frontier[x][1])
            Agent.scanArea((Agent.frontier[x][0],Agent.frontier[x][1]),board)
            #h = sqrt(pow((food[0] - Agent.frontier[x][0]),2) + pow((food[1] - Agent.frontier[x][1]),2))
            h = abs(food[0] - Agent.frontier[x][0]) + abs(food[1] - Agent.frontier[x][1])
            if(bodyClose):
                h = h - score*0.1
            if(foodClose):
                h = h - score*1.5
            if ((g+h) < cost):
                cost = g+h
                best = (Agent.frontier[x][0],Agent.frontier[x][1])
            elif((g+h) == cost and board[best[0]][best[1]] == GameObject.SNAKE_BODY):
                best = (Agent.frontier[x][0],Agent.frontier[x][1])


    def traceBack(board):
        Agent.key = food
        if(Agent.key in Agent.dict):
            while not(Agent.dict[Agent.key] == initial):
                Agent.key = Agent.dict[Agent.key]
                if not(Agent.key in Agent.dict):
                    Agent.randomMove(board)
                    return move


    def randomMove(board):
        x = initial[0]
        y = initial[1]
        best = (0,0)
        for i in range(0, len(list_man)):
            new_x = x+list_man[i][0]
            new_y = y+list_man[i][1]
            if(Agent.validMove(new_x, new_y)):
                if(board[new_x][new_y] == GameObject.FOOD):
                    Agent.determineMove(initialDirection, (new_x, new_y), initial)
                    break
                elif(board[new_x][new_y] == GameObject.EMPTY):
                    Agent.scanArea((new_x, new_y),board)
                    if(bodyClose or foodClose):
                        Agent.determineMove(initialDirection, (new_x, new_y), initial)
                        break
                    else:
                        best = (new_x,new_y)
        if not(best == (0,0)):
            Agent.determineMove(initialDirection, best, initial)


    def get_move(self, board, score, turns_alive, turns_to_starve, direction):
        global list_man, initialDirection, firstTime, t0
        if(len(Agent.timeList)==30):
            total_time = 0
            for x in range(0,len(Agent.timeList)):
                total_time = total_time + Agent.timeList[x]
            avg = total_time / len(Agent.timeList)
            print("average over", len(Agent.timeList), "trials with board size", Agent.board_height, "is:", avg)
            Agent.timeList = []

        if not(Agent.timerStarted):
            t0 = time.time()
            Agent.timerStarted = True
        firstTime = True
        initialDirection = direction
        Agent.currentDirection = direction
        #Get the position of the snake's head and the food object
        Agent.frontier = []
        Agent.closed = []
        Agent.dict = {}

        Agent.getSnakeHead(board)
        Agent.getFood(board)
        Agent.findBodyParts(board)

        while not(food == Agent.current):
            list_man = Agent.currentDirection.get_xy_moves()
            if (len(Agent.frontier) ==  0 and firstTime == False and len(Agent.closed) > 1):
                Agent.randomMove(board)
                return move
            elif (len(Agent.frontier) ==  0 and firstTime == False and len(Agent.closed) =< 1):
                return "Snakey died :("
        #In order to append the frontier with possible moves from the current posisiton of snake's head

            Agent.extendFrontier(board)
            firstTime = False
            Agent.mapPreviousPosition()
        #calculate the costs of possible moves according to A* Search
            Agent.determineBestMove(board,score)
            Agent.determineMove(Agent.currentDirection, best, Agent.current)
            Agent.setNewDirection()

        if(food == Agent.current):
            Agent.traceBack(board)
            Agent.determineMove(initialDirection, Agent.key, initial)
            return move



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
        t1 = time.time()
        print("time difference", t1-t0)
        Agent.timeList.append(t1-t0)
        Agent.timerStarted = False
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.
        """

        pass
