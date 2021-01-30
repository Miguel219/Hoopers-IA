from numpy import * 
from collections import namedtuple

from Square import Square
from Piece import Piece

#Tupla para las coordenadas del tablero
Coord = namedtuple('Coord',['x','y'])

class Game:
    def __init__(self, dimension = 10):
        #Tamaño del tablero
        self.dimension = dimension
        
        #tablero
        self.board = array([[None] * dimension] * dimension) 
        #Jugador 1
        self.player1 = None
        #Jugador 2
        self.player2 = None

        #Llenamos el tablero
        self.fillBoard(dimension)
        #Creamos los movimientos permitidos en las casillas
        self.setAllowedMovements()

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

