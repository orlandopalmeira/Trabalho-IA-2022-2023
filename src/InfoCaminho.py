
class InfoCaminho:
    """
    Classe que contém informação sobre o caminho que um algoritmo determinou.
    """
    def __init__(self , caminho_final, caminho_do_algoritmo):
        """
        Construtor da classe InfoCaminho
        :param caminho_final: caminho_final
        :param caminho_do_algoritmo: caminho_do_algoritmo
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
