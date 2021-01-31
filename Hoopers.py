from numpy import * 
from collections import namedtuple
from copy import deepcopy

from Square import Square
from Piece import Piece

#Tupla para las coordenadas del tablero
Coord = namedtuple('Coord',['x','y'])

class Game:
    def __init__(self, dimension = 10, state = 0, depth = 1, board = None, player1 = None, player2 = None):
        #Estado del juego
        self.state = state
        #Valor de la profundidad calculado por el alpha-beta-search del juego
        self.depth = depth
        #Tamaño del tablero
        self.dimension = dimension
        #tablero
        if board is not None:
            self.board = board 
        else:
            self.board = array([[None] * dimension] * dimension) 
        #Jugador 1
        self.player1 = player1
        
        #Jugador 2
        self.player2 = player2
        
        #Si es nuevo
        if board is None:
            #Llenamos el tablero
            self.fillBoard(dimension)
            #Creamos los movimientos permitidos en las casillas
            self.setAllowedMovements()

    #Avanza en la profundidad calculado por el alpha-beta-search del juego
    def advanceDepth(self):
        self.depth += 1

    #Crea las casillas y fichas de los jugadores y las coloca en las casillas correspondientes
    def fillBoard(self, dimension):
        #Calculo de piezas por jugador
        numberOfPieces = 0
        while(dimension > 0):
            numberOfPieces += int(dimension/2)
            dimension -= 2

        #Jugador 1
        self.player1 = array([None] * numberOfPieces)
        #Jugador 2
        self.player2 = array([None] * numberOfPieces)

        placedPiecesPlayer1 = 0
        placedPiecesPlayer2 = 0
        #Se llena el tablero 
        for y in range(self.dimension):          
            for x in range(self.dimension):
                if (x + y < (self.dimension/2) or x + y >= ((self.dimension/2) + self.dimension - 1)):
                    if (x + y < (self.dimension/2)):
                        newPiece = Piece(id='1-'+ str(placedPiecesPlayer1 + 1),position=Coord(x + 1,y + 1))
                        self.player1[placedPiecesPlayer1] = newPiece
                        self.board[y][x] = Square(position=Coord(x + 1,y + 1),visitor=newPiece)
                        placedPiecesPlayer1 += 1
                    else:
                        newPiece = Piece(id='2-'+ str(placedPiecesPlayer2 + 1),position=Coord(x + 1,y + 1))
                        self.player2[placedPiecesPlayer2] = newPiece
                        self.board[y][x] = Square(position=Coord(x + 1,y + 1),visitor=newPiece)
                        placedPiecesPlayer2 += 1
                else:
                    self.board[y][x] = Square(position=Coord(x + 1,y + 1))


    #Crea las relaciones entre las casillas 
    def setAllowedMovements(self):

        for row in self.board:
            for square in row:
                currentX, currentY = square.getPosition().x - 1, square.getPosition().y - 1
                #Se crean los movimientos
                if (currentX >= 1):
                    square.setLeft(self.board[currentY][currentX - 1])
                if (currentX <= self.dimension - 2):
                    square.setRight(self.board[currentY][currentX + 1])
                if (currentY <= self.dimension - 2):
                    square.setDown(self.board[currentY + 1][currentX])   
                if (currentY >= 1):
                    square.setUp(self.board[currentY - 1][currentX]) 
                if (currentX >= 1 and currentY <= self.dimension - 2):
                    square.setLeftDownDiagonal(self.board[currentY + 1][currentX - 1])
                if (currentX <= self.dimension - 2 and currentY <= self.dimension - 2):
                    square.setRightDownDiagonal(self.board[currentY + 1][currentX + 1])
                if (currentX >= 1 and currentY >= 1):
                    square.setLeftUpDiagonal(self.board[currentY - 1][currentX - 1])
                if (currentX <= self.dimension - 2  and currentY >= 1):
                    square.setRightUpDiagonal(self.board[currentY - 1][currentX + 1])

                #Se crean los saltos
                if (currentX > 1):
                    square.setHopLeft(self.board[currentY][currentX - 2])
                if (currentX < self.dimension - 2):
                    square.setHopRight(self.board[currentY][currentX + 2])
                if (currentY < self.dimension - 2):
                    square.setHopDown(self.board[currentY + 2][currentX])    
                if (currentY > 1):
                    square.setHopUp(self.board[currentY - 2][currentX])
                if (currentX > 1 and currentY < self.dimension - 2):
                    square.setHopLeftDownDiagonal(self.board[currentY + 2][currentX - 2])
                if (currentX < self.dimension - 2 and currentY < self.dimension - 2):
                    square.setHopRightDownDiagonal(self.board[currentY + 2][currentX + 2])
                if (currentX > 1 and currentY > 1):
                    square.setHopLeftUpDiagonal(self.board[currentY - 2][currentX - 2])
                if (currentX < self.dimension - 2  and currentY > 1):
                    square.setHopRightUpDiagonal(self.board[currentY - 2][currentX + 2])
    
    #Funcion que encuentra un camino de una casilla a otra casilla y cambia el estado del tablero
    def result(self, action, calculatePath = False):

        initialCoord, finalCoord = action
        
        for row in self.board:
            for square in row:
                square.setView(False)
        
        #Se crea una copia del juego
        newGame = deepcopy(self)

        #Se cambia la posición de la pieza del jugador
        for piece in newGame.toMove():
            if (piece.getPosition() == initialCoord):
                #Se cambia la posición de la pieza
                piece.setPosition(finalCoord)
                #Se cambia la posición de la pieza en el tablero
                newGame.board[initialCoord.y - 1][initialCoord.x - 1].setVisitor(None)
                newGame.board[finalCoord.y - 1][finalCoord.x - 1].setVisitor(piece)
        #Cambia de turno
        newGame.state = (newGame.state + 1) % 2
        
        #Si se quiere ver el path
        if (calculatePath):
            path = pathForSquareToFinalCoord(self.board[initialCoord.y - 1][initialCoord.x - 1], finalCoord)
            return newGame, (initialCoord, *path)
        else:
            return newGame, None

    #Funcion que devuelve el jugador que tiene el turno
    def toMove(self):
        if (self.state == 0):
            return self.player1
        elif (self.state == 1):
            return self.player2

    #Funcion que devuelve las acciones posibles del jugador que tiene el turno
    def actions(self):
        #Tupla con todas las acciones
        availableActions = tuple()
            
        for piece in self.toMove():
            x, y = piece.getPosition()
            square = self.board[y - 1][x - 1]
            availableActions = squaresToMove(square.getPosition(), square, availableActions)
        
        #Se devuelven las acciones ordenadas
        if (self.state == 0):
            return sorted(availableActions, key=lambda action : ((action[0].x + action[0].y) - (action[1].x + action[1].y)))
        if (self.state == 1):
            return sorted(availableActions, key=lambda action : ((action[1].x + action[1].y) - (action[0].x + action[0].y)))

    #Funcion que devuelve si el estado del juego es terminal 
    def isFinished(self):
        if (self.utility(self.player1,0)):
            countPlayer1 = self.utility(self.player1,0) + self.utility(self.player2,0)
            if (countPlayer1 == len(self.toMove()) - 1):
                return (True, 0, self.eval())
        if (self.utility(self.player2,1)):
            countPlayer2 = self.utility(self.player1,1) + self.utility(self.player2,1)
            if (countPlayer2 == len(self.toMove()) - 1):
                return (True, 1, self.eval())
        return (False, ) 
    
    #Funcion que devuelve si el estado del juego es terminal 
    def isTerminal(self):
        if self.utility(self.toMove()):
            countPiecesOnEnemysCamp = self.utility(self.player1, self.state) + self.utility(self.player2, self.state)
            if (countPiecesOnEnemysCamp == len(self.toMove()) - 1):
                return True
        return False

    #Funcion que devuelve si el estado del juego es el horizonte (Horizonte = 4)
    def isCutoff(self):
        if (self.depth > 4):
            return True
        else:
            return False

    #Funcion que devuelve la utility de un jugador
    def utility(self, player, state = None):
        if (state is None):
            state = self.state
        countPiecesOnEnemysCamp = 0
        for piece in player:
            x, y = piece.getPosition().x - 1, piece.getPosition().y - 1
            if (state == 1 and x + y < (self.dimension/2)):
                countPiecesOnEnemysCamp += 1
            if (state == 0 and x + y >= ((self.dimension/2) + self.dimension - 1)):
                countPiecesOnEnemysCamp += 1
        return countPiecesOnEnemysCamp 

    #Funcion que evalua los puntos de un estado del juego
    def eval(self):
        pointsPlayer1 = 0
        pointsPlayer2 = 0
        
        for piece in self.player1:
            x, y = piece.getPosition().x - 1, piece.getPosition().y - 1
            pointsPlayer1 = pointsPlayer1 + x + y 
        
        for piece in self.player2:
            x, y = ((self.dimension - 1) - (piece.getPosition().x - 1)), ((self.dimension - 1) - (piece.getPosition().y - 1))
            pointsPlayer2 = pointsPlayer2 + x + y

        return (pointsPlayer1 - pointsPlayer2)

    #Funcion que implementa el alpha-beta-search
    def alphaBetaSearch(self):
        value, move = maxValue(self, float('-inf'), float('inf'))
        return move
    
#Funcion que implementa el max-value
def maxValue(game, alpha, beta):
    if (game.isTerminal() or game.isCutoff()):
        return game.eval(), None
    v = float('-inf')
    for a in game.actions():
        newGame = game.result(a)[0]
        newGame.advanceDepth()
        v2, a2 = minValue(newGame, alpha, beta)
        if (v2 > v):
            v, move = v2, a
            alpha = max((alpha,v))
        if (v >= beta):
            return v, move
    return v, move

#Funcion que implementa el min-value
def minValue(game, alpha, beta):
    if (game.isTerminal() or game.isCutoff()):
        return game.eval(), None
    v = float('inf')
    for a in game.actions():
        newGame = game.result(a)[0]
        newGame.advanceDepth()
        v2, a2 = maxValue(newGame, alpha, beta)
        if (v2 < v):
            v, move = v2, a
            beta = min((beta,v))
        if (v <= alpha):
            return v, move
    return v, move
            

#Funcion que devuelve una tupla de las casillas a las que se puede mover una casilla
def squaresToMove(initialCoord, square, availableActions, recursive = False):
    #Revisa movimiento y salto a la izquierda
    if (square.getLeft()):
        if (square.getLeft().visitor):
            if (square.getHopLeft() and square.getHopLeft().visitor is None and (initialCoord, square.getHopLeft().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopLeft().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopLeft(), availableActions, recursive=True)
        elif((initialCoord, square.getLeft().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getLeft().getPosition()))

    #Revisa movimiento y salto a la derecha
    if (square.getRight()):
        if (square.getRight().visitor):
            if (square.getHopRight() and square.getHopRight().visitor is None and (initialCoord, square.getHopRight().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopRight().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopRight(), availableActions, recursive=True)
        elif((initialCoord, square.getRight().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getRight().getPosition()))

    #Revisa movimiento y salto hacia abajo
    if (square.getDown()):
        if (square.getDown().visitor):
            if (square.getHopDown() and square.getHopDown().visitor is None and (initialCoord, square.getHopDown().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopDown().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopDown(), availableActions, recursive=True)
        elif((initialCoord, square.getDown().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getDown().getPosition()))

    #Revisa movimiento y salto hacia arriba
    if (square.getUp()):
        if (square.getUp().visitor):
            if (square.getHopUp() and square.getHopUp().visitor is None and (initialCoord, square.getHopUp().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopUp().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopUp(), availableActions, recursive=True)
        elif((initialCoord, square.getUp().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getUp().getPosition()))

    #Revisa movimiento y salto hacia la diagonal izquierda abajo
    if (square.getLeftDownDiagonal()):
        if (square.getLeftDownDiagonal().visitor):
            if (square.getHopLeftDownDiagonal() and square.getHopLeftDownDiagonal().visitor is None and (initialCoord, square.getHopLeftDownDiagonal().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopLeftDownDiagonal().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopLeftDownDiagonal(), availableActions, recursive=True)
        elif((initialCoord, square.getLeftDownDiagonal().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getLeftDownDiagonal().getPosition()))

    #Revisa movimiento y salto hacia la diagonal derecha abajo
    if (square.getRightDownDiagonal()):
        if (square.getRightDownDiagonal().visitor):
            if (square.getHopRightDownDiagonal() and square.getHopRightDownDiagonal().visitor is None and (initialCoord, square.getHopRightDownDiagonal().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopRightDownDiagonal().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopRightDownDiagonal(), availableActions, recursive=True)
        elif((initialCoord, square.getRightDownDiagonal().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getRightDownDiagonal().getPosition()))

    #Revisa movimiento y salto hacia la diagonal izquierda arriba
    if (square.getLeftUpDiagonal()):
        if (square.getLeftUpDiagonal().visitor):
            if (square.getHopLeftUpDiagonal() and square.getHopLeftUpDiagonal().visitor is None and (initialCoord, square.getHopLeftUpDiagonal().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopLeftUpDiagonal().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopLeftUpDiagonal(), availableActions, recursive=True)
        elif((initialCoord, square.getLeftUpDiagonal().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getLeftUpDiagonal().getPosition()))

    #Revisa movimiento y salto hacia la diagonal derecha arriba
    if (square.getRightUpDiagonal()):
        if (square.getRightUpDiagonal().visitor):
            if (square.getHopRightUpDiagonal() and square.getHopRightUpDiagonal().visitor is None and (initialCoord, square.getHopRightUpDiagonal().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopRightUpDiagonal().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopRightUpDiagonal(), availableActions, recursive=True)
        elif((initialCoord, square.getRightUpDiagonal().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getRightUpDiagonal().getPosition()))

    return availableActions


#Funcion que devuelve una tupla de el camino de una casilla a otra casilla
def pathForSquareToFinalCoord(square, finalCoord, recursive = False):
    #Revisa movimiento y salto a la izquierda
    if (square.getLeft()):
        if (square.getLeft().visitor):
            if (square.getHopLeft() and square.getHopLeft().visitor is None):
                if (square.getHopLeft().getPosition() == finalCoord):
                    return (square.getHopLeft().getPosition(),)
                elif (square.getHopLeft().isView() == False):
                    square.getHopLeft().setView(True)
                    path = pathForSquareToFinalCoord(square.getHopLeft(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopLeft().getPosition(), *path)
        elif(not recursive):
            if (square.getLeft().getPosition() == finalCoord):
                    return (square.getLeft().getPosition(),)

    #Revisa movimiento y salto a la derecha
    if (square.getRight()):
        if (square.getRight().visitor):
            if (square.getHopRight() and square.getHopRight().visitor is None):
                if (square.getHopRight().getPosition() == finalCoord):
                    return (square.getHopRight().getPosition(),)
                elif (square.getHopRight().isView() == False):
                    square.getHopRight().setView(True)
                    path = pathForSquareToFinalCoord(square.getHopRight(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopRight().getPosition(), *path)
        elif(not recursive):
            if (square.getRight().getPosition() == finalCoord):
                    return (square.getRight().getPosition(),)

    #Revisa movimiento y salto hacia abajo
    if (square.getDown()):
        if (square.getDown().visitor):
            if (square.getHopDown() and square.getHopDown().visitor is None):
                if (square.getHopDown().getPosition() == finalCoord):
                    return (square.getHopDown().getPosition(),)
                elif (square.getHopDown().isView() == False):
                    square.getHopDown().setView(True)
                    path = pathForSquareToFinalCoord(square.getHopDown(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopDown().getPosition(), *path)
        elif(not recursive):
            if (square.getDown().getPosition() == finalCoord):
                    return (square.getDown().getPosition(),)

    #Revisa movimiento y salto hacia arriba
    if (square.getUp()):
        if (square.getUp().visitor):
            if (square.getHopUp() and square.getHopUp().visitor is None):
                if (square.getHopUp().getPosition() == finalCoord):
                    return (square.getHopUp().getPosition(),)
                elif (square.getHopUp().isView() == False):
                    square.getHopUp().setView(True)
                    path = pathForSquareToFinalCoord(square.getHopUp(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopUp().getPosition(), *path)
        elif(not recursive):
            if (square.getUp().getPosition() == finalCoord):
                    return (square.getUp().getPosition(),)

    #Revisa movimiento y salto hacia la diagonal izquierda abajo
    if (square.getLeftDownDiagonal()):
        if (square.getLeftDownDiagonal().visitor):
            if (square.getHopLeftDownDiagonal() and square.getHopLeftDownDiagonal().visitor is None):
                if (square.getHopLeftDownDiagonal().getPosition() == finalCoord):
                    return (square.getHopLeftDownDiagonal().getPosition(),)
                elif (square.getHopLeftDownDiagonal().isView() == False):
                    square.getHopLeftDownDiagonal().setView(True)
                    path = pathForSquareToFinalCoord(square.getHopLeftDownDiagonal(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopLeftDownDiagonal().getPosition(), *path)
        elif(not recursive):
            if (square.getLeftDownDiagonal().getPosition() == finalCoord):
                    return (square.getLeftDownDiagonal().getPosition(),)

    #Revisa movimiento y salto hacia la diagonal derecha abajo
    if (square.getRightDownDiagonal()):
        if (square.getRightDownDiagonal().visitor):
            if (square.getHopRightDownDiagonal() and square.getHopRightDownDiagonal().visitor is None):
                if (square.getHopRightDownDiagonal().getPosition() == finalCoord):
                    return (square.getHopRightDownDiagonal().getPosition(),)
                elif (square.getHopRightDownDiagonal().isView() == False):
                    square.getHopRightDownDiagonal().setView(True)
                    path = pathForSquareToFinalCoord(square.getHopRightDownDiagonal(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopRightDownDiagonal().getPosition(), *path)
        elif(not recursive):
            if (square.getRightDownDiagonal().getPosition() == finalCoord):
                    return (square.getRightDownDiagonal().getPosition(),)

    #Revisa movimiento y salto hacia la diagonal izquierda arriba
    if (square.getLeftUpDiagonal()):
        if (square.getLeftUpDiagonal().visitor):
            if (square.getHopLeftUpDiagonal() and square.getHopLeftUpDiagonal().visitor is None):
                if (square.getHopLeftUpDiagonal().getPosition() == finalCoord):
                    return (square.getHopLeftUpDiagonal().getPosition(),)
                elif (square.getHopLeftUpDiagonal().isView() == False):
                    square.getHopLeftUpDiagonal().setView(True)
                    path = pathForSquareToFinalCoord(square.getHopLeftUpDiagonal(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopLeftUpDiagonal().getPosition(), *path)
        elif(not recursive):
            if (square.getLeftUpDiagonal().getPosition() == finalCoord):
                    return (square.getLeftUpDiagonal().getPosition(),)

    #Revisa movimiento y salto hacia la diagonal derecha arriba
    if (square.getRightUpDiagonal()):
        if (square.getRightUpDiagonal().visitor):
            if (square.getHopRightUpDiagonal() and square.getHopRightUpDiagonal().visitor is None):
                if (square.getHopRightUpDiagonal().getPosition() == finalCoord):
                    return (square.getHopRightUpDiagonal().getPosition(),)
                elif (square.getHopRightUpDiagonal().isView() == False):
                    square.getHopRightUpDiagonal().setView(True)
                    path = pathForSquareToFinalCoord(square.getHopRightUpDiagonal(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopRightUpDiagonal().getPosition(), *path)
        elif(not recursive):
            if (square.getRightUpDiagonal().getPosition() == finalCoord):
                    return (square.getRightUpDiagonal().getPosition(),)

    return None