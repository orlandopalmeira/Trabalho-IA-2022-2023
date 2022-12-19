
class InfoCaminho:
    """
    Classe que contém informação sobre o caminho que um algoritmo determinou.
    """
    def __init__(self , caminho_final, caminho_do_algoritmo):
        """
        Construtor da classe InfoCaminho
        :param caminho_final: Lista de nodos que representam o caminho final
        :param caminho_do_algoritmo: Lista de nodos que representam o caminho do algoritmo
        """
        self.n_player = None
        self.nameofalgoritm = None
        self.caminhoFinal = caminho_final
        self.caminhoDoAlgoritmo = caminho_do_algoritmo


    def setnplayer(self, num: int):
        self.n_player = num

    def getnplayer(self):
        return self.n_player


    def setNameofAlgoritm(self, name):
        """
        :param name: String com o nome do algoritmo que foi utilizado.
        :return:
        """
        self.nameofalgoritm = name

    def setCaminhoFinal(self, caminho_final):
        self.caminhoFinal = caminho_final

    def setCaminhoDoAlgoritmo(self, caminho_do_algoritmo):
        self.caminhoDoAlgoritmo = caminho_do_algoritmo

    def getCaminhoFinal(self):
        return self.caminhoFinal

    def getCaminhoDoAlgoritmo(self):
        return self.caminhoDoAlgoritmo

    def existeCaminho(self):
        if len(self.caminhoFinal) == 0:
            return False
        else: return True

    def print(self, rp):
        """
        Printa no standard output toda a informação relativa ao caminho.
        :param rp: Recebe um objeto RaceP para poder calcular do caminho final, tendo em conta o grafo do problema.
        :return: Void
        """
        # Printagem do caminho do algoritmo.
        print(f"\nExpansão dos nós com o algoritmo {self.nameofalgoritm} do jogador {self.getnplayer()}: (lenght = {len(self.getCaminhoDoAlgoritmo())})")
        for p in self.getCaminhoDoAlgoritmo():
            print(p, end=" -> " if p != self.getCaminhoDoAlgoritmo()[-1] else " ")

        # Printagem do caminho final.
        if self.existeCaminho():
            print(
                f"\nCaminho final do jogador {self.getnplayer()} com o algoritmo {self.nameofalgoritm}: (lenght = {len(self.getCaminhoFinal())})")
            for p in self.getCaminhoFinal():
                print(p, end=" -> " if p != self.getCaminhoFinal()[-1] else " ")
            cost = rp.calcula_custo(self.getCaminhoFinal())
            print(f"\nCusto do caminho final do jogador {self.getnplayer()}: {cost}")
        else:
            print(f"\nCaminho para o jogador {self.getnplayer()} não foi encontrado!")

