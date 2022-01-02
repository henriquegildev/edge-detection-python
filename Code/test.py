from random import choices
from random import uniform
from operator import itemgetter
import time
import numpy as np
import glob
import scipy.ndimage
import imageio

start_time = time.time()


class DefinicoesClassificador:
    src_path = "./TestImages/Training"
    src_path_original = glob.glob(src_path + "/*/Original/*")
    src_path_perfect = glob.glob(src_path + "/*/Perfect/*")
    src_path_results = "./TestImages/Results/Images/"
    src_path_results_text = "./TestImages/Results/Text/"


"""
Função que busca todas as imagens dentro da pasta indicada
"""


def buscar_lista_de_treino(caminho):
    print(caminho)
    lista_de_treino = glob.glob(caminho + '/*')
    return lista_de_treino


"""
Função de custo, devolve a diferença entre a imagem perfeita e a imagem obtida pelo processo,
tendo em conta o tamanho da imagem.
"""


def comparar_imagens(perfeita, imperfeita):
    dif = np.abs(perfeita - imperfeita)
    res = np.sum(dif) / dif.size
    return res


"""
Nome: Gerar Genoma
Desc.: Gera genomas aleatórios
Input: None
Returns: 
"""


def gerar_genoma():
    return np.array([[uniform(-5.0, 5.0), uniform(-5.0, 5.0), uniform(-5.0, 5.0)], [0, 0, 0],
                     [uniform(-5.0, 5.0), uniform(-5.0, 5.0), uniform(-5.0, 5.0)]])


"""
Nome: Gerar N Genomas;
Desc.: Chama a função gerar_genoma N vezes, devolvendo uma lista com N genomas;
Input: N -> int;
"""


def gerar_populacao(n):
    return [gerar_genoma() for _ in range(n)]


"""
Nome: Selecionar da população
Desc.: Seleciona da população o top 10%
Input: populacao -> list(genoma); comparar_imagens -> original_image, processed_image; original_image -> np.array(float64); processed_image -> np.array(float64)
"""


def selecionar_da_populacao(populacao, comparar_imagens, perf, process):
    return choices(
        population=populacao,
        weights=[comparar_imagens(perf, process) for genoma in populacao],
        k=0.1 * len(populacao)
    )


if __name__ == '__main__':
    # lista_de_treino = buscar_lista_de_treino(DefinicoesClassificador.src_path_original)
    # print("Original Photos Paths: ", DefinicoesClassificador.src_path_original)
    # print("Perfect Photos Paths: ", DefinicoesClassificador.src_path_perfect)
    lista_de_treino = DefinicoesClassificador.src_path_original
    lista_matrizes_precisas = [[]]
    for ficheiro_de_imagem in lista_de_treino:
        index = lista_de_treino.index(ficheiro_de_imagem)
        print("Index: ", index, " File: ", ficheiro_de_imagem)

        # Leitura de imagem a processar, resultando num np.array
        imagem = imageio.imread(ficheiro_de_imagem)
        imagem_float = np.array(imagem, dtype=np.float64)  # Converter data type a float64

        lista_path = ficheiro_de_imagem.split('\\')
        nome = lista_path[-1]
        # Leitura de imagem perfeita, resultando num np.array
        imagem_perfeita = imageio.imread(DefinicoesClassificador.src_path_perfect[index])
        imagem_perfeita_float = np.array(imagem_perfeita, dtype=np.float64)
        lista_distancias = []
        lista_genomas = []
        # Aplicação de genoma
        # Time Complexity O(n)
        for genoma in gerar_populacao(1000):
            # Associar genomas a variáveis, sendo a Y transposta
            # hX = np.array([[-1.0, -2.0, -1.0], [0, 0, 0], [1.0, 2.0, 1.0]])
            hX = genoma
            hY = np.transpose(hX)

            gX = scipy.ndimage.convolve(imagem_float, hX)
            gY = scipy.ndimage.convolve(imagem_float, hY)
            g = np.abs(gX + gY)
            g_normal = g * (255.0 / (scipy.ndimage.maximum(g) - scipy.ndimage.minimum(g)))

            distancia = comparar_imagens(imagem_perfeita_float, g_normal)
            lista_genomas.append(hX)
            lista_distancias.append(distancia)
        # print(scipy.ndimage.minimum(g_normal), scipy.ndimage.maximum(g_normal))

        imageio.imwrite(DefinicoesClassificador.src_path_results + 'processed_{}'.format(nome),
                        g_normal.astype(np.uint8))
        # print(imagem.shape)
        # imageio.imwrite(DefinicoesClassificador.src_path_results + 'processed_{}'.format(nome),g_normal.astype(np.uint8))
        #print(nome, "| distancia: ", distancia)
        minimum = min(lista_distancias)
        pos = lista_distancias.index(minimum)
        lista_matrizes_precisas.append([minimum,lista_genomas[pos]])
        print("Minimum: ", minimum, "\n", "Matrix: ", lista_genomas[pos])
        print("--- Elapsed Time: %s seconds ---" % (time.time() - start_time))
        # print(imagem.shape)
lista_matrizes_precisas.remove([])
lista_matrizes_precisas.sort()
print(lista_matrizes_precisas[:1])
print("--- Final time: %s seconds ---" % (time.time() - start_time))
