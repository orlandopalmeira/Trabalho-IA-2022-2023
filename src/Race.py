from Node import Node

class RaceP:

    # Argumento "file_path" é o caminho para o ficheiro que contém o circuito.
    def __init__(self, file_path):
        self.g = {}
        self.matrix = {}
        self.start = None # tuplo da posição onde o jogador se encontra
        self.goals = []
        self.l = 0
        self.c = 0

        fp = open(file_path, "r")

        l = 0
        c = 0

        for line in fp:
            buf = []
            c = 0
            for ch in line:
                if ch != "\n":
                    if ch == "P":
                        self.start = (l,c)
                    if ch == "F":
                        self.goals.append((l,c))
                    buf.append(ch)
                    c += 1
            self.matrix[l] = buf
            l += 1

        self.l = len(self.matrix[0])
        self.c = len(self.matrix)


    def criaGrafo(self):
        start = self.start
        states = {} # posição: (vel, custo)
        visited = []
        estados = [(start, (0, 0), 0)] # posicao,

        while estados:
            p = estados.pop()
            visited.append(p)
            expansao = self.expand(p, vel, acc)

        pass


    def expand(self, pos, vel): # pos e vel do carro num determinado momento.

        accs = [(0,0), (1,0), (1,1), (0,1), (0,-1), (-1,0), (-1,-1), (1,-1), (-1,1)] # acelerações possíveis
        posicoes = []
        vels = []
        for ac in accs:
            # Calculo das novas velocidades dos eixos.
            new_vel_l = vel[0] + ac[0]
            new_vel_c = vel[1] + ac[1]

            # Calculo das novas posicoes dos eixos.
            new_pos_l = pos[0] + new_vel_l
            new_pos_c = pos[1] + new_vel_c

            # Formação da nova posiçao.
            new_pos = (new_pos_l, new_pos_c)
            new_vel = (new_vel_l, new_vel_c)
            if new_pos != pos and (0 <= new_pos[0] < self.l) and (0 <= new_pos[1] < self.c):
                posicoes.append(new_pos)
                vels.append(new_vel)

        return posicoes
        #return {"posicoes": posicoes, "velocidades": vels}

    def expande(self, estado: Node):
        """
        Esta função calcula os próximos estados possíveis dado um estado actual.
        """
        accs = [(0,0), (1,0), (1,1), (0,1), (0,-1), (-1,0), (-1,-1), (1,-1), (-1,1)] # acelerações possíveis
        estados = []

        for ac in accs:
            new = estado.clone()
            new.sumAll(new.velocity,ac)
            if new != estado and (0 <= new.position[0] < self.l) and (0 <= new.position[1] < self.c):
                estados.append(new)

        return estados

    def addAresta(self, from_node: Node, to_node: Node, custo: int):
        if from_node not in self.g:
            self.g[from_node] = [(custo,to_node)]
        else:
            self.g[from_node].append((custo,to_node))

    def cria_grafo(self):
        estados = []
        if self.start is not None:
            estados.append(Node(self.start,(0,0)))
        visitados = set()

        while estados:
            estado = estados.pop()
            visitados.add(estado)
            expansao = self.expande(estado)
            for e in expansao:
                if e not in visitados:
                    if self.possiblePath(estado.position,e.position): # verifica se é possível avancar, ou seja, não tem paredes pelo meio
                        self.addAresta(estado,Node(estado.position,(0,0)),25)
                    else:
                        self.addAresta(estado,e,1)
                    estados.append(e)


    def get_matrix(self):
        return self.matrix

    def get_start(self):
        return self.start

    def get_goals(self):
        return self.goals

    # Printa uma matriz com "H" nas posicoes indicadas.
    def print_matrix(self, posicoes, file="result.txt"):
        new_matrix = self.matrix
        for p in posicoes:
            l = p[0]
            c = p[1]
            new_matrix[l][c] = "H"

        fp = open(file, "w")
        for line_n in new_matrix:
            linha = "".join(new_matrix[line_n])
            fp.write(linha + "\n")
        fp.close()

    def obstaculo(self, coords: tuple) -> bool:
        """
        Indica se uma certa posição da matriz é um obstaculo ou não.
        """
        return self.matrix[coords[0]][coords[1]] == 'X'
    
    def possiblePath(self, pos_i: tuple, pos_f: tuple) :
        """
        Esta funcção verifica se é possível ir de uma posição para outra no mapa.
        Fonte: https://www.geeksforgeeks.org/check-possible-path-2d-matrix/
        """
        arr = []
        for i in range(len(self.matrix)):
            arr.append(self.matrix[i].copy())

        # directions
        Dir = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        # queue
        q = []
        # insert the initial position
        q.append((pos_i[0], pos_i[1]))
        # until queue is empty
        while(len(q) > 0) :
            p = q[0]
            q.pop(0)
            
            # mark as visited
            arr[p[0]][p[1]] = 'X'
            
            # destination is reached.
            if(p == (pos_f[0],pos_f[1])) :
                return True
                
            # check all four directions
            for i in range(4) :
                # using the direction array
                a = p[0] + Dir[i][0]
                b = p[1] + Dir[i][1]
                
                # not blocked and valid
                if(a >= pos_i[0] and b >= pos_i[1] and a <= pos_f[0] and b <= pos_f[1] and arr[a][b] != 'X') :           
                    q.append((a, b))
        return False


# Testing
rp = RaceP("race.txt")
matrix = rp.get_matrix()

list = rp.expand((3,1), (0,0))
print (list)
rp.print_matrix(list)

t = 0
