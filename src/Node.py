
class Node:
    def __init__(self ,position: tuple, velocity = (0,0)):
        self.position = position
        #self.velocity = velocity

    def setPosition(self, position: tuple):
        self.position = position

    def getPosition(self):
        return self.position

    def sumPosition(self, toAdd: tuple):
        self.position = (self.position[0] + toAdd[0], self.position[1] + toAdd[1])


    def clone(self):
        return Node(self.position)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o ,Node):
            return self.position[0] == __o.position[0] and self.position[1] == __o.position[1]
        else:
            return False

    def __str__(self) -> str:
        return f"[pos=({self.position[0]},{self.position[1]})]"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        tup = str(self.position)
        return hash(tup)

