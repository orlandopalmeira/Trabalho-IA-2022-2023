from queue import Queue
from Node import Node

import networkx as nx  # biblioteca de tratamento de grafos necessária para desnhar graficamente o grafo
import matplotlib.pyplot as plt  # idem


def get_positions_from_nodes(nodos):
    lista = []
    for nodo in nodos:
        lista.append(nodo.getPosition())
    return lista

def colorize(string, color):
    color_dict = {
        "red": "\033[1;91m",
        "green": "\033[1;92m",
        "yellow": "\033[1;93m",
        "purple": "\033[1;95m",
        "blue": "\033[1;96m",
        "white": "\033[1;97m",
    }
    endc = '\033[0m'
    color = color.lower()
    code = color_dict.get(color)
    if code is None:
        code = color_dict.get("white")
    res = code + string + endc
    return res


class RaceP:

    # Argumento "file_path" é o caminho para o ficheiro que contém o circuito.
    def __init__(self, file_path):
        self.g = {}
        self.g_directed = False
        self.g_h = {}  # eventuais heuristicas.
        self.matrix = {}
        self.start = None # tuplo da posição onde o jogador se encontra
        self.goals = []
        self.linhas = 0
        self.colunas = 0

        l = 0
        c = 0

        fp = open(file_path, "r")
        for line in fp:
            if not line.strip():
                continue  # ignora linhas em branco do ficheiro.
            buf = []
            c = 0
            for ch in line:
                if ch != "\n":
                    if ch == "P":
                        self.start = (l, c)
                    if ch == "F":
                        self.goals.append((l,c))
                    buf.append(ch)
                    c += 1
            self.matrix[l] = buf
            l += 1

        if self.start is None:
            print("Não foi definida uma posição inicial!")
            return
        self.linhas = len(self.matrix)
        self.colunas = len(self.matrix[0])


    def get_matrix(self):
        return self.matrix

    def get_start(self):
        return self.start

    def get_goals(self):
        return self.goals

    def get_value_in_graph(self, key_node):
        if self.g.get(key_node) is None:
            return []
        v = self.g.get(key_node)
        return v

    def get_cost_in_aresta(self, origin, dest):
        peso = 100000 ###
        for v in self.get_value_in_graph(origin):
            if v[1] == dest and v[0] < peso:
                peso = v[0]
        if peso == 100000:
            print("PROBLEMÁTICO!!")
        return peso


    def addAresta(self, from_node: Node, to_node: Node, custo = 1):
        if from_node not in self.g:
            self.g[from_node] = list()
        if to_node not in self.g:
            self.g[to_node] = list()

        self.g[from_node].append((custo,to_node))

        if not self.g_directed:
            self.g[to_node].append((custo, from_node))


    def cria_grafo(self):
        estados = [Node(self.start)]
        visitados = set()
        while estados:
            estado = estados.pop(0)
            visitados.add(estado)
            expansao = self.expande(estado)
            for e in expansao:
                if e not in visitados:
                    self.addAresta(estado, e, 1)
                    if e not in estados:
                        estados.append(e)


    def expande(self, estado: Node):
        x = estado.position[0]
        y = estado.position[1]
        poss = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        ret = []
        for tup in poss:
            nx = x+tup[0]
            ny = y+tup[1]
            position = (nx, ny)
            if not self.obstaculo(position) and self.canDiagPath(estado.position, position):
                ret.append(Node(position))
        return ret


    # Printa uma matriz com "*" nas posicoes dos nodos indicados.
    def print_matrix(self, caminho_de_nodos, file="result.txt"):
        if not caminho_de_nodos:
            print("Não foi encontrado nenhum caminho!")
            return

        # Faz clone da matriz.
        new_matrix = []
        for i in range(len(self.matrix)):
            new_matrix.append(self.matrix[i].copy())

        # retorna apenas os tuplos de posicao dos nodos.
        path = get_positions_from_nodes(caminho_de_nodos)

        it = 'a'
        for p in path:
            l = p[0]
            c = p[1]
            char = new_matrix[l][c]
            res = f"{it}"
            if char == "P":
                res = colorize(res, "red")
            elif char == "F":
                res = colorize(res, "blue")
            else:
                res = colorize(res, "green")
            new_matrix[l][c] = res
            it = chr(ord(it) + 1)

        #fp = open(file, "w")
        for line_n in new_matrix:
            linha = "".join(line_n)
            #fp.write(linha + "\n")
            print(linha)
        #fp.close()


    def obstaculo(self, coords: tuple) -> bool:
        """
        Indica se uma certa posição da matriz é um obstaculo ou não.
        """
        if self.linhas <= coords[0] or self.colunas <= coords[1]:
            return True
        b = self.matrix[coords[0]][coords[1]] == 'X'
        return b


    # Verifica a possibilidade de caminho na diagonal
    def canDiagPath(self, pos_i: tuple, pos_f: tuple):
        vel = (pos_f[0] - pos_i[0], pos_f[1] - pos_i[1])
        if vel != (0, 0) and abs(vel[0]) == abs(vel[1]):
            l = pos_i[0]
            c = pos_i[1]

            inc0 = vel[0] // abs(vel[0])
            inc1 = vel[1] // abs(vel[1])

            while True:
                if (l, c) == pos_f:
                    return True
                elif self.obstaculo((l, c)) or (self.obstaculo((l + inc0, c)) and self.obstaculo((l, c + inc1))):
                    return False
                l += inc0
                c += inc1

        return True

    # INUTIL COM A MUDANCA MAS TALVEZ A AUXILIAR DESTA SEJA UTIL.
    def possiblePath(self, pos_i: tuple, pos_f: tuple):
        """
        Esta funcção verifica se é possível ir de uma posição para outra no mapa.
        """
        vel = (pos_f[0] - pos_i[0], pos_f[1] - pos_i[1])

        if self.obstaculo(pos_f):
            return False

        if pos_i[0] == pos_f[0]:
            l = pos_i[0]
            menor = min(pos_i, pos_f, key=lambda x: x[1])
            maior = max(pos_i, pos_f, key=lambda x: x[1])
            for c in range(menor[1] + 1, maior[1]):
                if self.obstaculo((l, c)):
                    return False
            return True

        elif pos_i[1] == pos_f[1]:
            c = pos_i[1]
            menor = min(pos_i, pos_f, key=lambda x: x[0])
            maior = max(pos_i, pos_f, key=lambda x: x[0])
            for l in range(menor[0] + 1, maior[0]):
                if self.obstaculo((l, c)):
                    return False
            return True

        elif vel != (0,0) and abs(vel[0]) == abs(vel[1]):
            l=pos_i[0]
            c=pos_i[1]

            inc0 = vel[0] // abs(vel[0])
            inc1 = vel[1] // abs(vel[1])

            while True:
                if (l,c) == pos_f:
                    return True
                elif self.obstaculo((l,c)) or (self.obstaculo((l+inc0,c)) and self.obstaculo((l, c+inc1))):
                    return False
                l += inc0
                c += inc1

        # Para calcular a possibilidade de caminho nos casos em que as posicoes iniciais e finais não estao na mesma linha ou coluna.
        return self.__possiblePathAUX(pos_i, pos_f)


    def __possiblePathAUX(self, pos_i: tuple, pos_f: tuple) :
        """
        Esta funcção verifica se é possível ir de uma posição para outra no mapa.
        Fonte: https://www.geeksforgeeks.org/check-possible-path-2d-matrix/
        """
        if self.obstaculo(pos_f):
            return False

        arr = []
        for i in range(len(self.matrix)):
            arr.append(self.matrix[i].copy())

        # directions
        Dir = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        # queue, insert the initial position
        q = [pos_i]

        # until queue is empty
        while len(q) > 0 :
            p = q.pop(0)

            # mark as visited
            arr[p[0]][p[1]] = 'X'
            
            # destination is reached.
            if p == (pos_f[0],pos_f[1]) :
                return True
                
            # check all four directions
            for i in range(4) :
                # using the direction array
                a = p[0] + Dir[i][0]
                b = p[1] + Dir[i][1]
                
                # not blocked and valid
                if 0 <= a < self.linhas and 0 <= b < self.colunas and arr[a][b] != "X":
                    q.append((a, b))
        return False

    def calcula_custo(self, path):
        custo = 0
        if not path:
            return 0
        ant = path[0]
        for p in path[1:]:
            custo += self.get_cost_in_aresta(ant, p)
            ant = p
        return custo


    def desenha(self):
        ##criar lista de vertices
        lista_v = self.g.keys()
        lista_a = []
        g = nx.Graph()
        for nodo in lista_v:
            n = nodo.getName()
            g.add_node(n)
            for (peso, adjacente) in self.g[nodo]:
                lista = (n, adjacente)
                # lista_a.append(lista)
                g.add_edge(n, adjacente, weight=peso)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()


    def __procura_DFS(self,start: Node, end: list, path=[], visited=set()):
        path.append(start)
        visited.add(start)
        if start.position in end:
            return path

        for (_, adj) in self.g[start]:
            if adj not in visited and adj in self.g:
                resultado = self.__procura_DFS(adj, end, path, visited)
                if resultado is not None:
                    return resultado

        path.pop()  # se nao encontra remover o que está no caminho......
        return None


    def procura_DFS(self):
        return self.__procura_DFS(Node(self.start), self.goals, path = [], visited=set())


    def __procura_BFS(self, start, end):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()

        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        # garantir que o start node nao tem pais...
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual in end:
                path_found = True
            else:
                for (_, adjacente) in self.g[nodo_atual]:
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)

        # Reconstruir o caminho

        path = []
        end = nodo_atual
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # funçao calcula custo caminho
            
        return path


    def procura_BFS(self):
        s = Node(self.start)
        e = set([Node(x) for x in self.goals])
        return self.__procura_BFS(s,e)




'''
    # Funcão expande antiga com a capacidade de calcular as possibilidades de velocidade tendo em conta as aceleraçôes impostas.
    def expande(self, estado: Node):
        """
        Esta função calcula os próximos estados possíveis dado um estado atual.
        """
        accs = [(0,0), (1,0), (1,1), (0,1), (0,-1), (-1,0), (-1,-1), (1,-1), (-1,1)] # acelerações possíveis
        estados = []

        for ac in accs:
            new = estado.clone()
            new.sumVelocity(ac)
            new.sumPosition(new.velocity)
            if new != estado and (0 <= new.position[0] < self.linhas) and (0 <= new.position[1] < self.colunas):
                estados.append(new)

        return estados
    
    
    # Funcão cria_grafo antiga que tinha em conta as possibilidades diferentes de posição & velocidade.   
    def cria_grafo(self):
        estados = [Node(self.pos_inicial, (0, 0))]
        visitados = set()
        while estados:
            estado = estados.pop(0)
            visitados.add(estado)
            expansao = self.expande(estado)
            for e in expansao:
                if e not in visitados:
                    if not self.possiblePath(estado.position,e.position): # verifica se é possível avancar, ou seja, não tem paredes pelo meio
                        stopped_e = Node(estado.position, (0, 0))
                        if stopped_e not in visitados and ((25,stopped_e) not in self.get_value_in_graph(estado)):
                            self.addAresta(estado, stopped_e, 25)
                            if stopped_e not in estados:
                                estados.append(stopped_e)
                                #visitados.add(stopped_e)
                    else:
                        self.addAresta(estado,e,1)
                        if e not in estados:
                            estados.append(e)
                        #visitados.add(e)

'''

