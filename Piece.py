class Piece:
    def __init__(self, id, position):
        #Tamaño del tablero
        self.id = id
        #Posicion inicial en el tablero
        self.position = position

    #Get del color de la pieza
    def getId(self):
        return self.id

    #Get y Set de la posición de la pieza
    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def __str__(self):
        return str(self.id)