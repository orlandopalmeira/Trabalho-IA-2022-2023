import sys
import time

from Race import RaceP

def verify_same_element(list1, list2):
	"""
	Retorna None no caso de não haver correspondencias. Caso contrário retorna o primeiro indice onde os elementos são iguais.
	:return:
	"""
	for i in range(len(list1)):
		if list1[i] == list2[i]:
			return i
		return None

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
            print("Wrong input!")
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
                print(f"**** Algoritmos para o jogador {n_player} ****")
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

            # TODO verificação de colisoes.


            # Itera todos os caminhos finais dos carros.
            for caminho in info_caminhos:

                print(f"\nExpansão dos nós com o algoritmo {caminho.nameofalgoritm} do jogador {caminho.getnplayer()}:")
                for p in caminho.getCaminhoDoAlgoritmo():
                    print(p, end=" ")
                if caminho.existeCaminho():
                    print(f"\nCaminho final do jogador {caminho.getnplayer()} com o algoritmo {caminho.nameofalgoritm}:")
                    for p in caminho.getCaminhoFinal():
                        print(p, end=" ")
                    cost = rp.calcula_custo(caminho.getCaminhoFinal())
                    print(f"\nCusto do caminho final do jogador {caminho.getnplayer()}: {cost}")
                else:
                    print(f"\nCaminho para o jogador {caminho.getnplayer()} não foi encontrado!")
                #print(f"Com o tempo: {duracao}ms")

            print("\nImagem dos caminhos:")
            rp.print_caminhos(info_caminhos)
            enter = input("Prima enter para continuar.")


        # DFS
        elif saida == 6:
            start = time.time()
            caminho = rp.procura_DFS(rp.start[0])
            end = time.time()
            duracao = (end-start) * 1000
            cost = rp.calcula_custo(caminho)
            if caminho:
                for p in caminho:
                    print(p)
                print(f"Com o custo: {cost}\nCom o tempo: {duracao}ms")

            print("\nFez o seguinte caminho:")
            rp.print_caminho(caminho)
            enter = input("Prima enter para continuar.")

        # BFS
        elif saida == 7:
            start = time.time()
            caminho = rp.procura_BFS(rp.start[0])
            end = time.time()
            duracao = (end-start) * 1000
            cost = rp.calcula_custo(caminho)
            if caminho:
                for p in caminho:
                    print(p)
                print(f"Com o custo: {cost}\nCom o tempo: {duracao}ms")

            print("\nFez o seguinte caminho:")
            rp.print_caminho(caminho)
            enter = input("Prima enter para continuar.")

        # Greedy
        elif saida == 8:
            start = time.time()
            paths = rp.greedy(rp.start[0])
            end = time.time()
            duracao = (end-start) * 1000
            for caminho in paths:
                cost = rp.calcula_custo(caminho)
                if caminho:
                    for p in caminho:
                        print(p)
                    print(f"Com o custo: {cost}\nCom o tempo: {duracao}ms")

            print("\nFez o seguinte caminho:")
            rp.print_caminhos(paths)
            enter = input("Prima enter para continuar.")

        # A*
        elif saida == 9:
            start = time.time()
            caminho = rp.procura_aStar(rp.start[0])
            end = time.time()
            duracao = (end-start) * 1000
            cost = rp.calcula_custo(caminho)
            if caminho:
                for p in caminho:
                    print(p)
                print(f"Com o custo: {cost}\nCom o tempo: {duracao}ms")

            print("\nFez o seguinte caminho:")
            rp.print_caminho(caminho)
            enter = input("Prima enter para continuar.\n")
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