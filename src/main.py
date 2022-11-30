import sys
from Race import RaceP


def main():

    circuit = input("Indique a path do ficheiro do circuito-> ")

    try:
        rp = RaceP(circuit)
    except FileNotFoundError:
        print("File not found!")
        sys.exit(0)
    rp.cria_grafo()
    saida = -1

    while saida != 0:
        print("1-Imprimir Grafo ")
        print("2-Desenhar Grafo")
        print("3-Indicar posições inicial e finais do circuito")
        print("4-Imprimir nodos do Grafo")
        print("5-DFS")
        print("6-BFS")
        print("0-Sair")

        try:
            saida = int(input("Introduza a sua opcão-> "))
        except ValueError:
            print("Wrong input!")
            l = input("Prima enter para continuar.")
            continue
        if saida == 0:
            print("A sair...")
        elif saida == 1:
            for it in rp.g:
                print(f"{it} -> {rp.g[it]}")
            l=input("Prima enter para continuar.")
        elif saida == 2:
            rp.desenha()
        elif saida == 3:
            print(f"Posição Inicial -> {rp.get_start()}")
            print(f"Posições Finais/Metas -> {rp.get_goals()}")
            l = input("Prima enter para continuar.")
        elif saida == 4:
            for k in rp.g.keys():
                print(k)
            l = input("Prima enter para continuar.")
        elif saida == 5:
            path = rp.procura_DFS()
            cost = rp.calcula_custo(path)
            if path:
                for p in path:
                    print(p)
                print(f"Com o custo: {cost}")
            # Printa as posições em que passa no caminho no ficheiro result.txt e no stdout.
            print("\nFez o seguinte caminho:")
            rp.print_matrix(path)
            l = input("Prima enter para continuar.")
        elif saida == 6:
            path = rp.procura_BFS()
            cost = rp.calcula_custo(path)
            if path:
                for p in path:
                    print(p)
                print(f"Com o custo: {cost}")
            # Printa as posições em que passa no caminho no ficheiro result.txt e no stdout.
            print("\nFez o seguinte caminho:")
            rp.print_matrix(path)
            l = input("Prima enter para continuar.")
        else:
            print("Wrong input!")
            l = input("Prima enter para continuar.")


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