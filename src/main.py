import math
import sys
import time

from Race import RaceP
from Node import Node
from InfoCaminho import InfoCaminho

def min_vel(t1, t2):
    """
    Retorna o indice do menor tuplo de velocidade (Exemplo: t1 < t2, retorna 0, caso contrario 1).
    :param t1: Tuplo de velocidade
    :param t2: Tuplo de velocidade
    :return: Retorna o indice do menor tuplo de velocidade.
    """
    x1, y1 = t1
    x2, y2 = t2
    t1 = math.sqrt(x1**2 + y1**2)
    t2 = math.sqrt(x2**2 + y2**2)
    if t1 < t2:
        return 0
    else:
        return 1

def verify_same_element(cam1, cam2):
    """
    Retorna um tuplo (indice_colisao, indice da lista onde vao ocorrer as alteraçoes)
    :param cam1: Objeto InfoCaminho 1
    :param cam2: Objeto InfoCaminho 2
    :return: Retorna um tuplo (indice_colisao, ind_change(0 ou 1 sendo o indice da lista que vai ser alterada)).
    """
    list1 = cam1.caminhoFinal
    list2 = cam2.caminhoFinal
    for i in range(min(len(list1), len(list2))):
        if list1[i] == list2[i]:
            if cam1.velocidades or cam2.velocidades:
                vel0 = cam1.velocidades[i]
                vel1 = cam2.velocidades[i]
                min_ind = min_vel(vel0, vel1)
                return i, min_ind
            else:
                return i, 0 # Para o caso de não haver velocidades.
    return None, None

def insert_list_in_index(lista, index, list_to_insert):
    """
    Insere uma lista numa lista num determinado indice, removendo o valor do indice original.
    :param lista: Lista original.
    :param index: Indice onde queremos inserir a lista_to_insert na lista.
    :param list_to_insert: Lista que queremos inserir.
    :return: Resultado da inserção da lista.
    """
    del lista[index]
    for i in list_to_insert:
        lista.insert(index, i)
        index += 1
    return lista

def main():

    #circuit = input("Indique a path do ficheiro do circuito: ")
    circuit = "race.txt" # FIXME Maneira mais rápida para testar. Alterar no final.
    #circuit = "raceold.txt"
    try:
        rp = RaceP(circuit)
    except FileNotFoundError:
        print("Circuit file not found!")
        sys.exit(0)
    except AssertionError as exc:
        print(exc)
        sys.exit(0)


    rp.cria_grafo()
    rp.heuristicaManhDistance()

    saida = -1
    while saida != 0:
        print("\n**** Menu ****")
        print("1-Imprimir Grafo ")
        print("2-Desenhar Grafo")
        print("3-Indicar posições inicial e finais do circuito")
        print("4-Imprimir nodos do Grafo")
        print("5-Aplicar algoritmos aos carros")
        """
        print("6-DFS")
        print("7-BFS")
        print("8-Greedy")
        print("9-A*")
        """
        print("0-Sair")

        try:
            saida = int(input("Introduza a sua opcão: "))
        except ValueError:
            print("\nWrong input!")
            enter = input("Prima enter para continuar.")
            continue

        if saida == 0:
            print("\nA sair...")

        # Imprimir Grafo
        elif saida == 1:
            for it in rp.g:
                print(f"{it} -> {rp.g[it]}")
            enter=input("Prima enter para continuar.")

        # Desenhar Grafo
        elif saida == 2:
            rp.desenha()

        # Indicar posições inicial e finais do circuito
        elif saida == 3:
            print(f"Posição Inicial -> {rp.get_start()}")
            print(f"Posições Finais/Metas -> {rp.get_goals()}")
            enter = input("Prima enter para continuar.")

        # Imprimir nodos do Grafo
        elif saida == 4:
            for k in rp.g.keys():
                print(k)
            enter = input("Prima enter para continuar.")

        # Utilizar algoritmos
        elif saida == 5:
            n_player = 0
            player_algoritms = []
            name_algoritms = []
            for player in rp.start:
                print(f"\n**** Algoritmo para o jogador {n_player} ****")
                print("1-DFS")
                print("2-BFS")
                print("3-Greedy")
                print("4-A*")
                #print("0-Sair")
                while True:
                    try:
                        saida = int(input("Introduza a sua opcão: "))
                        if saida not in [1,2,3,4]:
                            raise ValueError
                        break
                    except ValueError:
                        print("Input inválido!")
                        #enter = input("Prima enter para continuar.")
                        #continue
                if saida == 1:
                    player_algoritms.append(rp.procura_DFS)
                    name_algoritms.append("DFS")
                elif saida == 2:
                    player_algoritms.append(rp.procura_BFS)
                    name_algoritms.append("BFS")
                elif saida == 3:
                    player_algoritms.append(rp.greedy)
                    name_algoritms.append("Greedy")
                elif saida == 4:
                    player_algoritms.append(rp.procura_aStar)
                    name_algoritms.append("A*")

                n_player += 1

            n_player: int = 0
            info_caminhos = []

            # Cria as informações dos caminhos requisitados. Objetos InfoCaminho na variavél info_caminhos.
            for algoritmo in player_algoritms: # "algoritmo" é o algoritmo que se vai correr para um determinado jogador.
                returnedCaminho = algoritmo(rp.start[n_player]) # exemplo -> rp.greedy((3,2)). In which "algoritmo" = rp.greedy.
                returnedCaminho.setnplayer(n_player)
                returnedCaminho.setNameofAlgoritm(name_algoritms[n_player])
                info_caminhos.append(returnedCaminho)
                n_player += 1

            # Verificação de colisoes.
            ########################################
            if len(info_caminhos) > 1:
                cam1 = [Node((4,4)), Node((4,5)), Node((4,6)), Node((4,7)), Node((4,8))]
                cam1 = InfoCaminho(cam1, [])
                cam2 = [Node((3,4)), Node((4,5)), Node((3,6)), Node((3,7))]
                cam2 = InfoCaminho(cam2, [])
                ########################################
                colisao: int = 0
                # colisao = verify_same_element(info_caminhos[0], info_caminhos[1])
                colisao, ind_change = verify_same_element(cam1, cam2)
                while colisao is not None and colisao != len(info_caminhos[ind_change].caminhoFinal) - 1:
                    print(f"Ocorreu colisão em {colisao}. Menor velocidade no indice {ind_change}. Recalculando caminho...")
                    #changing_caminho = info_caminhos[ind_change].caminhoFinal
                    changing_caminho = cam2  #### FIXME (REMOVER E DESCOMENTAR LINHA EM CIMA) Escolha de caminho hardcoded para debug com caminhos fixos.
                    lista_de_nodos = changing_caminho.getCaminhoFinal() # Passa do objeto Infocaminho para uma lista de nodos.
                    desvio = rp.procura_BFS(lista_de_nodos[colisao - 1].position, lista_de_nodos[colisao + 1], lista_de_nodos[colisao])
                    desvio = desvio.getCaminhoFinal()[1:-1] # Caminho alternativo encontrado.
                    insert_list_in_index(lista_de_nodos, colisao, desvio) # altera o path para o path com o desvio.
                    changing_caminho.setCaminhoFinal(lista_de_nodos) # insere o novo caminho no InfoCaminho.

                    # Re-verificação de colisões.
                    # colisao = verify_same_element(info_caminhos[0], info_caminhos[1])
                    colisao, ind_change = verify_same_element(cam1, cam2)

                # TODO verificação de colisoes. ((END))

            # Itera todos os caminhos finais dos carros.
            for caminho in info_caminhos:
                caminho.print(rp)

            print("\nImagem dos caminhos:")
            rp.print_caminhos(info_caminhos)
            enter = input("Prima enter para continuar.")

        else:
            print("Wrong input!")
            enter = input("Prima enter para continuar.")


if __name__ == "__main__":
    main()
    pass


'''
# Testing
rp = RaceP("race.txt")
rp.cria_grafo()

# Printa o caminho e o custo para o stdout.
caminho = rp.procura_BFS()
custo = rp.calcula_custo(caminho)
if caminho:
    for n in caminho:
        print(n)
print(f"Custo do caminho: {custo}")

# Printa as posições em que passa no caminho no ficheiro result.txt
rp.print_matrix(caminho)

# Desenha o grafo n vezes.
# for i in range(10): rp.desenha()

print("Done")
'''