class Square:
    def __init__(self, position, visitor = None):
        #Posición en el  tablero
        self.position = position
        #Valor calculado
        self.value = None
        #Ficha en su lugar
        self.visitor = visitor
        #Movimientos
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.leftUpDiagonal = None
        self.rightUpDiagonal = None
        self.leftDownDiagonal = None
        self.rightDownDiagonal = None
        #Saltos
        self.hopLeft = None
        self.hopRight = None
        self.hopUp = None
        self.hopDown = None
        self.hopLeftUpDiagonal = None
        self.hopRightUpDiagonal = None
        self.hopLeftDownDiagonal = None
        self.hopRightDownDiagonal = None

    #Get de la posición de la casilla
    def getPosition(self):
        return self.position

    #Get y Set del value de la casilla
    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    #Get y Set del value de la casilla
    def getVisitor(self):
        return self.visitor

    def setVisitor(self, visitor):
        self.visitor = visitor

    #Gets y Sets de movimientos
    def getLeft(self):
        return self.left
        
    def setLeft(self, square):
        self.left = square

    def getRight(self):
        return self.right
        
    def setRight(self, square):
        self.right = square

    def getUp(self):
        return self.up
        
    def setUp(self, square):
        self.up = square
        
    def getDown(self):
        return self.down
        
    def setDown(self, square):
        self.down = square
        
    def getLeftUpDiagonal(self):
        return self.leftUpDiagonal
        
    def setLeftUpDiagonal(self, square):
        self.leftUpDiagonal = square
        
    def getRightUpDiagonal(self):
        return self.rightUpDiagonal
        
    def setRightUpDiagonal(self, square):
        self.rightUpDiagonal = square
        
    def getLeftDownDiagonal(self):
        return self.leftDownDiagonal
        
    def setLeftDownDiagonal(self, square):
        self.leftDownDiagonal = square
        
    def getRightDownDiagonal(self):
        return self.rightDownDiagonal
        
    def setRightDownDiagonal(self, square):
        self.rightDownDiagonal = square

    #Get de saltos
    def getHopLeft(self):
        return self.hopLeft
        
    def setHopLeft(self, square):
        self.hopLeft = square

    def getHopRight(self):
        return self.hopRight
        
    def setHopRight(self, square):
        self.hopRight = square
        
    def getHopUp(self):
        return self.hopUp
        
    def setHopUp(self, square):
        self.hopUp = square
        
    def getHopDown(self):
        return self.hopDown
        
    def setHopDown(self, square):
        self.hopDown = square
        
    def getHopLeftUpDiagonal(self):
        return self.hopLeftUpDiagonal
        
    def setHopLeftUpDiagonal(self, square):
        self.hopLeftUpDiagonal = square
        
    def getHopRightUpDiagonal(self):
        return self.hopRightUpDiagonal
        
    def setHopRightUpDiagonal(self, square):
        self.hopRightUpDiagonal = square
        
    def getHopLeftDownDiagonal(self):
        return self.hopLeftDownDiagonal
        
    def setHopLeftDownDiagonal(self, square):
        self.hopLeftDownDiagonal = square
        
    def getHopRightDownDiagonal(self):
        return self.hopRightDownDiagonal
        
    def setHopRightDownDiagonal(self, square):
        self.hopRightDownDiagonal = square

    def __str__(self):
        if (self.visitor):
            return str(self.position) + ' | Visitante: ' + str(self.visitor)
        else:
            return str(self.position)