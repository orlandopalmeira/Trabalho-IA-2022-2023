from queue import Queue
from Node import Node
from InfoCaminho import InfoCaminho
import math
import networkx as nx  # biblioteca de tratamento de grafos necessária para desnhar graficamente o grafo
import matplotlib.pyplot as plt  # idem
import numpy

numpy.seterr(divide='ignore')
numpy.seterr(invalid='ignore')

INF = 100000

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
        self.matrix = {}
        self.g_h = {}  # heuristicas.
        #self.start = None # tuplo da posição onde o jogador se encontra
        self.start = []
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
                        self.start.append((l,c))
                    if ch == "F":
                        self.goals.append((l,c))
                    buf.append(ch)
                    c += 1
            self.matrix[l] = buf
            l += 1

        if len(self.start) == 0:
            raise AssertionError("Não foi definida uma posição inicial!")
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
            print("PROBLEMÁTICO!!") # Debug
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
        for pos in self.start: # Faz-se a expansão do grafo com começo em todas as start positions para o caso de alguma start position estiver numa ilha.
            estados = [Node(pos)]
            visitados = set()
            while estados:
                estado = estados.pop(0)
                visitados.add(estado)
                expansao = self.expande(estado)
                for e in expansao:
                    pos_i = estado.position
                    pos_f = e.position
                    if e not in visitados:
                        self.addAresta(estado, e, 1)
                        if e not in estados:
                            estados.append(e)


    def expande(self, estado: Node):
        x = estado.position[0]
        y = estado.position[1]
        #poss = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        poss = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

        ret = []
        for p in poss:
            newx = x + p[0]
            newy = y + p[1]
            position = (newx, newy)
            if not self.obstaculo(position) and self.canDiagPath(estado.position, position):
                ret.append(Node(position))
        return ret


    def print_caminho(self, info_caminho: InfoCaminho):
        """
        Desenha numa matriz, o caminho fornecido.
        :param info_caminho: Objeto InfoCaminho que contém informação sobre os caminhos.
        :return: void
        """
        if not info_caminho.existeCaminho():
            print("Não foi encontrado nenhum caminho!")
            return

        # Faz clone da matriz.
        new_matrix = []
        for i in range(len(self.matrix)):
            new_matrix.append(self.matrix[i].copy())


        # retorna apenas os tuplos de posicao dos nodos.
        path = get_positions_from_nodes(info_caminho.getCaminhoFinal())

        l,c = path[0]
        new_matrix[l][c] = colorize("a", "red")
        step = 'b'
        for p in path[1:]:
            l,c = p
            char = new_matrix[l][c]
            res = f"{step}"
            if char == "F":
                res = colorize(res, "blue")
            else:
                res = colorize(res, "green")
            new_matrix[l][c] = res
            step = chr(ord(step) + 1) if step != "z" else "a"

        for line_n in new_matrix:
            linha = "".join(line_n)
            print(linha)


    def print_caminhos(self, infocaminhos):
        """
        Printa os caminhos finais de todos os infoCaminhos.
        :param infocaminhos: Lista de objetos infoCaminho
        :return: void
        """

        # Faz clone da matriz.
        new_matrix = []
        for i in range(len(self.matrix)):
            new_matrix.append(self.matrix[i].copy())

        i = 0
        colors = ["green", "yellow", "purple", "blue", "red"]
        n_player = 0
        for infoCam in infocaminhos:
            if not infoCam.existeCaminho():
                #print("Não foi encontrado nenhum caminho!")
                continue
            color = colors[i]
            i = i + 1 if i != 4 else 0 # Para rodar o indice que percorre o array das diferentes cores disponiveis.

            # retorna apenas os tuplos de posicao dos nodos.
            path = get_positions_from_nodes(infoCam.getCaminhoFinal())

            step = 'a'
            for p in path:
                l = p[0]
                c = p[1]
                char = new_matrix[l][c]
                res = f"{step}"
                if char == "P":
                    res = colorize(res, "red")
                elif char == "F":
                    res = colorize(res, "blue")
                else:
                    res = colorize(res, color)
                new_matrix[l][c] = res
                step = chr(ord(step) + 1) if step != "z" else "a"

        # Printa a matriz final com os caminhos de todos desenhados.
        for line_n in new_matrix:
            linha = "".join(line_n)
            print(linha)


    def obstaculo(self, coords: tuple) -> bool:
        """
        Indica se uma certa posição da matriz é um obstaculo ou não.
        """
        if self.linhas <= coords[0] or self.colunas <= coords[1]:
            return True
        b = self.matrix[coords[0]][coords[1]] == 'X'
        return b


    def canDiagPath(self, pos_i: tuple, pos_f: tuple):
        """
        Verifica a possibilidade de caminho na diagonal.
        :param pos_i: posição inicial
        :param pos_f: posição final
        :return: void
        """
        vetor = (pos_f[0] - pos_i[0], pos_f[1] - pos_i[1])
        if vetor != (0, 0) and abs(vetor[0]) == abs(vetor[1]):
            l = pos_i[0]
            c = pos_i[1]

            inc0 = vetor[0] // abs(vetor[0])
            inc1 = vetor[1] // abs(vetor[1])

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
        Esta função verifica se é possível ir de uma posição para outra no mapa.
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
        Esta função verifica se é possível ir de uma posição para outra no mapa.
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
        """
        Utiliza a biblioteca networkx para desenhar a estrutura do grafo utilizado no nosso problema.
        :return:
        """
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


    def procura_DFS(self, start: tuple):
        """
        Algoritmo DFS.
        :param path: Caminho feito
        :param visited: Nodos visitados.
        :param start: Tuplo que indica a posição onde começa o algoritmo.
        :return: Objeto InfoCaminho que contem informação sobre o caminho determinado pelo algoritmo.
        """
        return self.__procura_DFS(Node(start), self.goals, path = [], visited = [])

    def __procura_DFS(self,start: Node, end: list, path=[], visited=[]):
        path.append(start)
        if start not in visited:
            visited.append(start)
        #self.print_caminho(path) ### TO PRINT THE WAY STEP BY STEP.
        #print()
        if start.position in end:
            return InfoCaminho(path, visited)
            #return path

        for (_, adj) in self.g[start]:
            if adj not in visited and adj in self.g:
                resultado = self.__procura_DFS(adj, end, path, visited)
                if resultado.existeCaminho():
                    return resultado

        path.pop()  # se nao encontra remover o que está no caminho......
        #return None
        return InfoCaminho([], visited)


    def procura_BFS(self, start: tuple, end:Node = None, toAvoid:Node = None):
        """
        Aplica o Algoritmo BFS ao jogador indicado pelo indice(n_player).
        :param start: Tuplo que indica a posição onde começa o algoritmo.
        :param end: Tuplo que indica o nodo destino. Se não tiver nada, os destinos finais são os indicados por "F" no ficheiro.
        :param toAvoid: Nodo a evitar.
        :return: Objeto InfoCaminho que contem informação sobre o caminho determinado pelo algoritmo.
        """
        s = Node(start)
        if end is None:
            e = set([Node(x) for x in self.goals])
        else:
            e = [end]

        return self.__procura_BFS(s,e, toAvoid)

    def __procura_BFS(self, start, end, toAvoid:Node = None):
        # definir nodos visitados para evitar ciclos

        visited = {toAvoid}
        #visited = set([toAvoid])
        fila = Queue()

        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        # Lista onde vão ser armazenados os nodos que o algoritmo percorre.
        caminho_do_algoritmo = []

        # garantir que o start node nao tem pais...
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            caminho_do_algoritmo.append(nodo_atual)
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
        return InfoCaminho(path, caminho_do_algoritmo)


    def in_tuple_distance(self, nodo):
        """
        Calcula a distância num tuplo do nodo à meta mais próxima.
        :param nodo: Node
        :return: tuple
        """
        res = 1000000
        pos = nodo.getPosition()
        x = pos[0]
        y = pos[1]
        candidates = []
        for g in self.goals:
            gx = g[0]
            gy = g[1]
            new = (gx-x, gy-y)
            candidates.append(new)
        #dists = map(lambda v: math.sqrt((v[0]) ** 2 + (v[1]) ** 2), candidates)
        #minim = candidates[dists.index(min(dists))]
        minim = min(candidates, key=lambda v: math.sqrt((v[0]) ** 2 + (v[1]) ** 2))
        return minim


    def euclidian_distance(self, nodo):
        """
        Calcula a distância euclidiana do nodo à meta mais próxima.
        :param nodo: Node
        :return: inteiro
        """
        res = 1000000
        pos = nodo.getPosition()
        x = pos[0]
        y = pos[1]
        for g in self.goals:
            gx = g[0]
            gy = g[1]
            new = math.sqrt((x-gx) ** 2 + (y-gy) ** 2)
            if new < res: res = new
        return res

    def manhatan_distance(self, nodo):
        """
        Calcula a distância de manhatan do nodo fornecido no argumento ao destino final mais próximo.
        :param nodo: Node
        :return: inteiro
        """
        res = 1000000
        pos = nodo.getPosition()
        x = pos[0]
        y = pos[1]
        for g in self.goals:
            gx = g[0]
            gy = g[1]
            new = abs(gx-x)+abs(gy-y)
            if new < res: res = new
        return res

    def heuristicaManhDistance(self):
        """
        Define a heuristica dos nodos através da sua distância de Manhattan ao destino mais perto.
        :return: void
        """
        nodos = self.g.keys()
        for n in nodos:
            self.g_h[n] = self.manhatan_distance(n)


    def getH(self, nodo):
        if nodo not in self.g_h.keys():
            return 10000
        else:
            return self.g_h[nodo]

    def getNeighbours(self, nodo):
        lista = []
        for (custo, adjacente) in self.g[nodo]:
            lista.append((custo, adjacente))
        return lista

    def heurisitic_velocity(self, current_node:Node, next_node:Node, vel: tuple):
        """
        Função que permite o cálculo dinâmico de heuristicas relativamente à velocidade.
        :param current_node: Nodo atual, necessário para o calculo da nova velocidade.
        :param next_node: Nodo cuja heuristica queremos verificar.
        :param vel: Velocidade da posição atual a ter em conta no calculo da heuristica.
        :return: Valor heuristico do nodo.
        """
        #distance = self.euclidian_distance(next_node)
        distance = self.in_tuple_distance(next_node)
        acc = tuple(numpy.subtract(next_node.position, current_node.position))
        next_vel = tuple(numpy.add(vel, acc))
        #next_vel = math.sqrt(next_vel[0] ** 2 + next_vel[1] ** 2)

        #time_estimate = distance / next_vel
        time_estimate = tuple(numpy.divide(distance, next_vel))
        new_tx, new_ty = time_estimate
        if new_tx < 0:
            new_tx *= -INF
        elif math.isnan(new_tx):
            new_tx = 0
        if new_ty < 0:
            new_ty *= -INF
        elif math.isnan(new_ty):
            new_ty = 0
        time_estimate = (new_tx, new_ty)
        time_estimate = new_tx + new_ty

        return time_estimate


    def greedy(self, start: tuple):
        """
        Aplica o Algoritmo Greedy ao jogador indicado pelo indice(n_player).
        :param start: Tuplo que indica a posição onde começa o algoritmo.
        :return: Objeto InfoCaminho que contem informação sobre o caminho determinado pelo algoritmo
        """
        s = Node(start)
        e = set([Node(x) for x in self.goals])
        return self.__greedy(s, e)

    def __greedy(self, start, end):
        """
        Algoritmo greedy
        :param start: Nodo inicial
        :param end: Nodos finais
        :return: Objeto InfoCaminho que contem informação sobre o caminho determinado pelo algoritmo
        """
        # open_list é uma lista de nodos visitados, mas com vizinhos que ainda não foram todos visitados, começa com o start
        # closed_list é uma lista de nodos visitados
        # e todos os seus vizinhos também já o foram
        open_list = {start}
        closed_list = set([])

        # Lista onde vão ser armazenados os nodos que o algoritmo percorre.
        caminho_do_algoritmo = []

        # Lista de tuplo que faz match com o caminho do algoritmo, e indica as velocidades do carro, na determinada posição.
        historico_de_velocidades = []

        # Dicionário que guarda informação dos pais dos nodos.
        parents = {start: start}

        velocidade = (0,0)
        nodoAnterior = start
        while len(open_list) > 0:
            # encontra nodo com a menor heuristica
            n = None
            for v in open_list:
                #if n is None or self.g_h[v] < self.g_h[n]:
                if n is None or self.heurisitic_velocity(nodoAnterior, v, velocidade) < self.heurisitic_velocity(nodoAnterior, n, velocidade):
                    n = v

            acc = tuple(numpy.subtract(n.position, nodoAnterior.position))
            nodoAnterior = n
            velocidade = tuple(numpy.add(velocidade, acc))

            caminho_do_algoritmo.append(n)
            historico_de_velocidades.append(velocidade)

            if n is None:
                #print('Path does not exist!')
                return InfoCaminho([], caminho_do_algoritmo)

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor
            if n in end:
                caminho_final = []
                while parents[n] != n:
                    caminho_final.append(n)
                    n = parents[n]
                caminho_final.append(start)
                caminho_final.reverse()
                ### MATCHING DAS VELOCIDADES COM O CAMINHO FINAL ### # FIXME - por enquanto isto é inutil.
                i = 0
                new_hist_vel = []
                for node,velocidade in zip(caminho_do_algoritmo, historico_de_velocidades):
                    if caminho_final[i] == node:
                        i += 1
                        new_hist_vel.append(velocidade)
                #################################################
                caminho = InfoCaminho(caminho_final, caminho_do_algoritmo, historico_de_velocidades)
                return caminho

            # para todos os vizinhos do nodo corrente
            for (_, adjacente) in self.getNeighbours(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if adjacente not in open_list and adjacente not in closed_list:
                    open_list.add(adjacente)
                    parents[adjacente] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        #print('Path does not exist!')
        return InfoCaminho([], caminho_do_algoritmo)


    def procura_aStar(self, start: tuple):
        """
        Aplica o Algoritmo AStar ao jogador indicado pelo indice(n_player).
        :param start: Tuplo que indica a posição onde começa o algoritmo.
        :return: Objeto InfoCaminho que contem informação sobre o caminho determinado pelo algoritmo
        """
        s = Node(start)
        e = set([Node(x) for x in self.goals])
        return self.__procura_aStar(s, e)

    def __procura_aStar(self, start, end):
        open_list = {start}
        closed_list = set([])

        # g contains current distances from start_node to these nodes
        # the default value (if it's not found in the map) is +infinity
        g = {start: 0}

        # Lista que guardará todos os nodos que o algoritmo percorre.
        caminho_do_algoritmo = []

        historico_de_velocidades = []

        # parents contains an adjacency map of all nodes
        parents = {start: start}

        velocidade = (0,0)
        nodoAnterior = start
        n = None
        while len(open_list) > 0:
            # find a node with the lowest value of f() - evaluation function
            calc_heurist = {}
            flag = 0
            for v in open_list:
                if n is None:
                    n = v
                else:
                    flag = 1
                    #calc_heurist[v] = g[v] + self.getH(v)
                    hv = self.heurisitic_velocity(nodoAnterior, v, velocidade)
                    calc_heurist[v] = g[v] + hv

            if flag == 1:
                min_estima = min(calc_heurist, key=calc_heurist.get) # retorna o nodo que tem menor heuristica.
                #min_estima1 = self.calcula_est(calc_heurist)
                n = min_estima
                #print(f"Escolhido -> {n}", end= "\n\n")

            if n is None:
                return InfoCaminho([], caminho_do_algoritmo)

            acc = tuple(numpy.subtract(n.position, nodoAnterior.position))
            nodoAnterior = n
            velocidade = tuple(numpy.add(velocidade, acc))

            caminho_do_algoritmo.append(n)
            historico_de_velocidades.append(velocidade)

            # if the current node is the stop_node
            # then we begin reconstructing the path from it to the start_node
            if n in end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()

                ### MATCHING DAS VELOCIDADES COM O CAMINHO FINAL ###
                i = 0
                new_hist_vel = []
                for node, velocidade in zip(caminho_do_algoritmo, historico_de_velocidades):
                    if reconst_path[i] == node:
                        i += 1
                        new_hist_vel.append(velocidade)
                #################################################
                return InfoCaminho(reconst_path, caminho_do_algoritmo, historico_de_velocidades)

            # for all neighbors of the current node do
            for (custo, adjacente) in self.getNeighbours(n):  # definir função getneighbours  tem de ter um par nodo peso
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if adjacente not in open_list and adjacente not in closed_list:
                    open_list.add(adjacente)
                    parents[adjacente] = n
                    g[adjacente] = g[n] + custo

                # otherwise, check if it's quicker to first visit n, then "adjacente"
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[adjacente] > g[n] + custo:
                        g[adjacente] = g[n] + custo
                        parents[adjacente] = n

                        if adjacente in closed_list:
                            closed_list.remove(adjacente)
                            open_list.add(adjacente)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        return InfoCaminho([], caminho_do_algoritmo)







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

