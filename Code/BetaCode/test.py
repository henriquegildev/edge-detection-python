import prettyprint
import random
from datetime import datetime
import time
import numpy as np
import glob
import scipy.ndimage
import imageio
import threading

global lock
lock = threading.Lock()
randint = random.randint
global rng
rng = np.random.default_rng()


class DefinicoesClassificador:
    src_path = "./TestImages/Training"  # Diretorio de todas as imagens de treino
    src_path_testing = "./TestImages/Test"
    # Diretorio das images de treino originais
    src_path_original = glob.glob(src_path + "/*/Original/*")
    # Diretorio das images de treino perfeitas
    src_path_perfect = glob.glob(src_path + "/*/Perfect/*")
    # Diretorio das images de teste originais
    src_path_original_test = glob.glob(src_path_testing + "/*/Original/*")
    # Diretorio das images de teste perfeitas
    src_path_perfect_test = glob.glob(src_path_testing + "/*/Perfect/*")
    # Diretorio das images de treino resultantes
    src_path_results = "./TestImages/Results/Images/"
    # Diretorio do ficheiro .txt com informação relativa ao treino
    src_path_results_text = "./TestImages/Results/Text/"
    src_path_recover = "./TestImages/Recover/"


"""
Função que busca todas as imagens dentro da pasta indicada
"""


def buscar_lista_teste(caminho):
    lista_de_teste = glob.glob(caminho + '/*')
    return lista_de_teste


"""
Função de custo, devolve a diferença entre a imagem perfeita e a imagem obtida pelo processo,
tendo em conta o tamanho da imagem.
"""


def compare_images(perfect, imperfect):
    dif = np.abs(perfect - imperfect)
    res = np.sum(dif) / dif.size
    return res


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
    # print("Old population size: {} ~ New population size: {}".format(len(populacao), len(new_pop)))
    return new_pop


def apply_genome(genome, g_normals, genome_list, distance_list, image_float, perfect_image_float):
    # input: genome, g_normals, lista_genome, distance_list image_float, image_float_perfeita,y
    # alterado: genome_list, distance_list g_normals
    hX = genome
    hY = np.transpose(hX)  # Obtem a matriz transposta de hX(genome)

    # Convolução da imagem pelo genome
    gX = scipy.ndimage.convolve(image_float, hX)
    # Convolução da imagem pela transposição do genome
    gY = scipy.ndimage.convolve(image_float, hY)
    # Obter o valor absoluto da soma dos arrays trabalhados
    g = np.abs(gX + gY)
    g_normal = g * (255.0 / (scipy.ndimage.maximum(g) -
                             scipy.ndimage.minimum(g)))

    distance = compare_images(perfect_image_float, g_normal)
    # LOCK
    lock.acquire()  # Lock
    genome_list.append(hX)
    distance_list.append(distance)
    g_normals.append(g_normal)
    lock.release()  # Release
    # UNLOCK

"""
Nome: Buscar Genoma 
Desc.: Recupera o melhor genoma obtido pelos treinos
Input: num_file: int
Returns: 
"""


def buscar_genoma():
    input_file = open("../TestImages/Recover/gene.txt", 'r')
    gene_tmp = []
    next(input_file) # Jumps to second line, since first line contains best result of operator
    for i in input_file:
        gene_tmp.append(float(i))
    gene = np.array([gene_tmp[:3], [0, 0, 0], gene_tmp[3:]])
    return gene


if __name__ == '__main__':
    # num_file = len(glob.glob(ClassifierDefinitions.src_path_results_text + 'results*.txt'))
    test_list = DefinicoesClassificador.src_path_original_test
    print(test_list)
    prettyprint.start_animation()
    num_images = len(test_list)
    image_float = []
    perfect_image_float = []
    path_list = []
    nome = []

    for image_file in test_list:
        path_list.append(image_file.split('\\'))
        nome.append(path_list[-1][-1])
        index = test_list.index(image_file)
        # Leitura de image a processar, resultando num np.array
        image_float.append(
            np.array(imageio.imread(image_file), dtype=np.float64))  # Converter data type a float64

        # Leitura de image perfeita, resultando num np.array
        perfect_image_float.append(
            np.array(imageio.imread(DefinicoesClassificador.src_path_perfect_test[index]), dtype=np.float64))

    genome = buscar_genoma()
    distance_list = []
    genome_list = []
    g_normals = []
    for i in range(num_images):
        prettyprint.set_text("Index: {}/100 | File: {}".format(i + 2, nome[i], ))
        thread = threading.Thread(target=apply_genome, args=(genome, g_normals, genome_list,
                                                             distance_list, image_float[i],
                                                             perfect_image_float[i],))
        thread.start()
    while threading.active_count() > 2:
        pass

    low = min(distance_list)
    # ploting.animate(i, low)
    # output_file.write(
    #     "Minimum: {} | Iteration: {}/{} | File: {} \n Matrix: {}\n".format(low[0], i + 1,
    #                                                                        iterations, nome[y], low[1]))
    # output_file.write("--- Final Time: {:4f} seconds ---".format(time.time() - start_time))
    # output_file.close()
    prettyprint.stop_animation()
    print("Lowest distance, ", low)

    #print("--- Final time: %s seconds ---" % (time.time() - start_time))
