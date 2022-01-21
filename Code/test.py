import datetime
import random
import sys
import traceback
from random import choices
from random import uniform
from datetime import datetime
import time
import numpy as np
import glob
import scipy.ndimage
import imageio


randint = random.randint
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


def encher_populacao(n, populacao):
    for i in range(n):
        populacao.append(gerar_genoma())
    return populacao


"""
Nome: Selecionar da população
Desc.: Seleciona da população o top 10%
Input: populacao -> list(genoma); comparar_imagens -> original_image, processed_image; original_image -> np.array(float64); processed_image -> np.array(float64)
"""


def selecionar_da_populacao(n: int, populacao: list):
    new_pop = []
    populacao.sort()
    new_pop_temp = populacao[:int(n * 0.1)]
    for i in new_pop_temp:
        new_pop.append(i[1])
    # print(new_pop)
    print("Old population size: {} ~ New population size: {}".format(len(populacao), len(new_pop)))
    return new_pop


"""
Nome: Crossover
Desc.: Seleciona da população o top 10%
Input: populacao -> list(genoma); comparar_imagens -> original_image, processed_image; original_image -> np.array(float64); processed_image -> np.array(float64)
"""

#Implementar evolucao da funcao de custo
#Crossover fazer de 1-5 com distribuicao centrada no 3
#Fazer swap fixo, mas quais sao
def crossover(populacao: list):
    combinations = {}
    new_pop = []
    index = 0
    for i in populacao:
        combinations[index] = []
        pos = randint(0, len(populacao) - 1)
        try:
            if pos in combinations:
                while index in combinations[pos]:
                    pos = randint(0, len(populacao) - 1)
        except KeyError as err:
            print("Something happened: ", err)
            traceback.print_exc()
        combinations[index].append(pos)
        rand = populacao[pos]
        g1_a, g1_b, g2_a, g2_b = list(i[0]), list(i[2]), list(rand[0]), list(rand[2])
        list_genesA, list_genesB = [g1_a, g2_a], [g1_b, g2_b]
        listA, listB = [[], []], [list_genesA, list_genesB]
        for par in range(0, 2):
            for x in range(0, 3):
                pos1 = randint(0, len(list_genesA) - 1)
                gene = listB[par][pos1]
                pos2 = randint(0, len(gene) - 1)
                chr = gene[pos2]
                listA[par].append(chr)
        new_gene = np.array([listA[0], [0, 0, 0], listA[1]])
        new_pop.append(new_gene)
        index += 1
    # print(new_pop)
    return new_pop

if __name__ == '__main__':
    index = 0
    num_file = len(glob.glob(DefinicoesClassificador.src_path_results_text + 'results*.txt'))
    output_file = open(DefinicoesClassificador.src_path_results_text + "results{}.txt".format(num_file + 1), 'w')
    lista_de_treino = DefinicoesClassificador.src_path_original
    iterations = 10

    populacao = gerar_populacao(10)
    size_of_pop = len(populacao)
    output_file.write(
        "Run Begin Time: {} | Run Number: {} | Projected Iterations: {} | Size of Population: {}\n".format(datetime.now(),
                                                                                                         num_file,
                                                                                                         iterations,
                                                                                                         size_of_pop))
    for i in range(0, iterations):
        print("New Cycle - Iteration: {}/{}".format(i + 1, iterations))
        media_val = []
        populacao_results = []
        for ficheiro_de_imagem in lista_de_treino:
            lista_path = ficheiro_de_imagem.split('\\')
            nome = lista_path[-1]
            index = lista_de_treino.index(ficheiro_de_imagem)
            print("Iterations: {}/{} | Index: {}/200 | File: {}".format(i + 1, iterations, index, nome))

            # Leitura de imagem a processar, resultando num np.array
            imagem = imageio.imread(ficheiro_de_imagem)
            imagem_float = np.array(imagem, dtype=np.float64)  # Converter data type a float64


            # Leitura de imagem perfeita, resultando num np.array
            imagem_perfeita = imageio.imread(DefinicoesClassificador.src_path_perfect[index])
            imagem_perfeita_float = np.array(imagem_perfeita, dtype=np.float64)
            lista_distancias = []
            lista_genomas = []
            # Aplicação de genoma
            # Time Complexity O(n)
            for genoma in populacao:
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

            imageio.imwrite(DefinicoesClassificador.src_path_results + 'processed_{}'.format(nome),
                            g_normal.astype(np.uint8))
            minimum = min(lista_distancias)
            media_val.append(minimum)
            pos = lista_distancias.index(minimum)
            populacao_results.append([minimum, lista_genomas[pos]])
            # print("Minimum: ", minimum, "\n", "Matrix: ", lista_genomas[pos])
            print(" Elapsed Time: {:4f} seconds | Minimum: {}".format(time.time() - start_time, minimum))
            print("Average Fitness: {}".format(sum(media_val) / len(media_val)))
            output_file.write(
                "Average Fitness: {} | Iteration: {}/{} | File: {} \n".format((sum(media_val) / len(media_val)), i + 1, iterations, nome))
        populacao_tmp = selecionar_da_populacao(size_of_pop, populacao_results)
        populacao = crossover(populacao_tmp)
        encher_populacao(int(0.9 * size_of_pop), populacao)

output_file.write("--- Final Time: {:4f} seconds ---".format(time.time() - start_time))
output_file.close()
print("--- Final time: %s seconds ---" % (time.time() - start_time))
