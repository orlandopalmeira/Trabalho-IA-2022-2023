from Race import RaceP

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



def main():

    rp = RaceP("race.txt")
    rp.cria_grafo()
    saida = -1

    while saida != 0:
        print("1-Imprimir grafo ")
        print("2-Desenhar Grafo")
        print("3-Imprimir  nodos de Grafo")
        print("4-Imprimir arestas de Grafo")
        print("5-DFS")
        print("6-BFS")
        print("7 -Outra solução ")
        print("0-Saír")

        saida = int(input("introduza a sua opcao-> "))
        if saida == 0:
            print("saindo.......")
        elif saida == 1:
            for it in rp.g:
                print(f"{it} -> {rp.g[it]}")
            l=input("Prima enter para continuar.")
        elif saida == 2:
            rp.g.desenha()
        elif saida == 3:
            print(rp.g.m_graph.keys())
            l = input("Prima enter para continuar.")
        elif saida == 4:
            print(rp.g.imprime_aresta())
            l = input("Prima enter para continuar.")
        elif saida == 5:
            inicio=input("Nodo inicial->")
            fim = input("Nodo final->")
            caminho=rp.solucaoDFS(inicio, fim)
            print(caminho)
            if caminho != None:
               a = caminho[0]
               lista=rp.imprimeA(a)
               print(lista)
            l = input("Prima enter para continuar.")
        elif saida == 6:
            inicio = input("Nodo inicial->")
            fim = input("Nodo final->")
            caminho=rp.solucaoBFS(inicio, fim)
            print(caminho)
            if caminho != None:
                a = caminho[0]
                lista = rp.imprimeA(a)
                print(lista)
            l = input("Prima enter para continuar.")
        elif saida == 7:
            inicio = input("Nodo inicial->")
            fim = input("Nodo final->")
            caminho = rp.encontraDFS(inicio, fim)
            print(caminho)
            if caminho != None:
                a = caminho[0]
                lista = rp.imprimeA(a)
                print(lista)
            l = input("Prima enter para continuar.")
        else:
            print("Wrong input!")
            l = input("Prima enter para continuar.")


if __name__ == "__main__":
    main()
    pass
