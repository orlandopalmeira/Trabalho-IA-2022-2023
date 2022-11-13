
class Node:
    def __init__(self ,position: tuple, velocity: tuple):
        self.position = position
        self.velocity = velocity

    def setPosition(self, position: tuple):
        self.position = position

    def setVelocity(self, velocity: tuple):
        self.velocity = velocity

    def getPosition(self):
        return self.position

    def getVelocity(self):
        return self.velocity

    def setAll(self, position: tuple, velocity: tuple):
        self.setPosition(position)
        self.setVelocity(velocity)

    def sumPosition(self, toAdd: tuple):
        self.position = (self.position[0] + toAdd[0], self.position[1] + toAdd[1])

    def sumVelocity(self, toAdd: tuple):
        self.velocity = (self.velocity[0] + toAdd[0], self.velocity[1] + toAdd[1])

    def clone(self):
        return Node(self.position ,self.velocity)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o ,Node):
            return self.position[0] == __o.position[0] and self.position[1] == __o.position[1] and self.velocity[0] == __o.velocity[0] and self.velocity[1] == __o.velocity[1]
        else:
            return False

    def __str__(self) -> str:
        return f"[pos=({self.position[0]},{self.position[1]}),vel=({self.velocity[0]},{self.velocity[1]})]"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        tup = (self.position,self.velocity)
        return hash(tup)

