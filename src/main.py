import sys
import time

from Race import RaceP


def main():

    #circuit = input("Indique a path do ficheiro do circuito: ")
    circuit = "race.txt" # FIXME Maneira mais rápida para testar. Alterar no final.
    circuit = "raceold.txt"
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
        print("\n****Menu****")
        print("1-Imprimir Grafo ")
        print("2-Desenhar Grafo")
        print("3-Indicar posições inicial e finais do circuito")
        print("4-Imprimir nodos do Grafo")
        print("5-DFS")
        print("6-BFS")
        print("7-Greedy")
        print("8-A*")
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
        elif saida == 10:
            player_algoritms = []
            for player in rp.start:
                print("1-DFS")
                print("2-BFS")
                print("3-Greedy")
                print("4-A*")
                print("0-Sair")
                saida = 99
                while saida == 99:
                    try:
                        saida = int(input("Introduza a sua opcão: "))
                    except ValueError:
                        print("Wrong input!")
                        enter = input("Prima enter para continuar.")
                        continue
                if saida == 1:
                    player_algoritms.append(rp.procura_DFS())
                if saida == 2:
                    player_algoritms.append(rp.procura_BFS())
                if saida == 3:
                    player_algoritms.append(rp.greedy())
                if saida == 4:
                    player_algoritms.append(rp.procura_aStar())


        # DFS
        elif saida == 5:
            start = time.time()
            path = rp.procura_DFS()
            end = time.time()
            duracao = (end-start) * 1000
            cost = rp.calcula_custo(path)
            if path:
                for p in path:
                    print(p)
                print(f"Com o custo: {cost}\nCom o tempo: {duracao}ms")

            print("\nFez o seguinte caminho:")
            rp.print_matrix(path)
            enter = input("Prima enter para continuar.")

        # BFS
        elif saida == 6:
            start = time.time()
            path = rp.procura_BFS()
            end = time.time()
            duracao = (end-start) * 1000
            cost = rp.calcula_custo(path)
            if path:
                for p in path:
                    print(p)
                print(f"Com o custo: {cost}\nCom o tempo: {duracao}ms")

            print("\nFez o seguinte caminho:")
            rp.print_matrix(path)
            enter = input("Prima enter para continuar.")

        # Greedy
        elif saida == 7:
            start = time.time()
            paths = rp.greedy()
            end = time.time()
            duracao = (end-start) * 1000
            for path in paths:
                cost = rp.calcula_custo(path)
                if path:
                    for p in path:
                        print(p)
                    print(f"Com o custo: {cost}\nCom o tempo: {duracao}ms")

            print("\nFez o seguinte caminho:")
            rp.print_caminhos(paths)
            enter = input("Prima enter para continuar.")

        # A*
        elif saida == 8:
            start = time.time()
            path = rp.procura_aStar()
            end = time.time()
            duracao = (end-start) * 1000
            cost = rp.calcula_custo(path)
            if path:
                for p in path:
                    print(p)
                print(f"Com o custo: {cost}\nCom o tempo: {duracao}ms")

            print("\nFez o seguinte caminho:")
            rp.print_matrix(path)
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