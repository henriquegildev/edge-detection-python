# import ploting

import prettyprint
import random
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
    src_path = "./TestImages/Test"  # Diretorio de todas as imagens de trieno
    # Diretorio das images de teste originais
    src_path_original = glob.glob(src_path + "/*/Original/*")
    # Diretorio das images de teste perfeitas
    src_path_perfect = glob.glob(src_path + "/*/Perfect/*")
    # Diretorio das images de teste resultantes
    src_path_results = "./TestImages/Results/Images/TestResults/Images/"
    # Diretorio do ficheiro .txt com informação relativa ao teste
    src_path_results_text = "./TestImages/Results/TestResults/Text/"


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


def comparar_imagens(perfeita, imperfeita):
    dif = np.abs(perfeita - imperfeita)
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


"""
Nome: apply_genoma
Desc.: Aplica o genoma
Input: genoma, g_normals, lista_genoma, lista_distancia, imagem_float, imagem_float_perfeita,y
"""


def apply_genoma(genoma, g_normals, lista_genomas, lista_distancias, imagem_float, imagem_perfeita_float):
    # input: genoma, g_normals, lista_genoma, lista_distancia, imagem_float, imagem_float_perfeita,y
    # alterado: lista_genomas, lista_distancia, g_normals
    hX = genoma
    hY = np.transpose(hX)  # Obtem a matriz transposta de hX(genoma)

    # Convolução da imagem pelo genoma
    gX = scipy.ndimage.convolve(imagem_float, hX)
    # Convolução da imagem pela transposição do genoma
    gY = scipy.ndimage.convolve(imagem_float, hY)
    # Obter o valor absoluto da soma dos arrays trabalhados
    g = np.abs(gX + gY)
    g_normal = g * (255.0 / (scipy.ndimage.maximum(g) -
                    scipy.ndimage.minimum(g)))

    distancia = comparar_imagens(imagem_perfeita_float, g_normal)
    # LOCK
    lock.acquire()  # Lock
    lista_genomas.append(hX)
    lista_distancias.append(distancia)
    g_normals.append(g_normal)
    lock.release()  # Release
    # UNLOCK


"""
Nome: Buscar Genoma 
Desc.: Recupera o melhor genoma obtido pelos treinos
Input: num_file: int
Returns: 
"""


def buscar_genoma(num_file):
    input_file = open("./TestImages/Recover/gene.txt", 'r')
    gene_tmp = []
    # Jumps to second line, since first line contains best result of operator
    next(input_file)
    for i in input_file:
        gene_tmp.append(float(i))
    gene = np.array([gene_tmp[:3], [0, 0, 0], gene_tmp[3:]])
    return gene


if __name__ == '__main__':
    index = 0
    num_file = len(
        glob.glob(DefinicoesClassificador.src_path_results_text + 'results*.txt'))
    # Ficheiro .txt usado para armazenar informação relativa ao teste realizado
    output_file = open(DefinicoesClassificador.src_path_results_text +
                       "results{}.txt".format(num_file + 1), 'w+')
    # Lista com as fotos de teste originais
    lista_de_teste = DefinicoesClassificador.src_path_original
    iterations = 10  # Número de iterações a ser realizadas
    minimum = "None"

    output_file.write(
        "Run Begin Time: {} | Run Number: {} | Projected Iterations: {}\n".format(
            datetime.now(),
            num_file,
            iterations))

    prettyprint.start_animation()
    total_img = len(lista_de_teste)
    imagem_raw = []
    imagem_float = []
    imagem_perfeita = []
    imagem_perfeita_float = []
    lista_path = []
    nome = []
    lowest = []

    for ficheiro_de_imagem in lista_de_teste:
        # Lista para divir o diretorio de cada ficheiro um array
        lista_path.append(ficheiro_de_imagem.split('\\'))
        # Buscar o valor do array que represneta o nome do ficheiro
        nome.append(lista_path[-1][-1])
        index = lista_de_teste.index(ficheiro_de_imagem)
        # Leitura de imagem a processar, resultando num np.array
        imagem_float.append(
            np.array(imageio.imread(ficheiro_de_imagem), dtype=np.float64))  # Converter data type a float64

        # Leitura de imagem perfeita, resultando num np.array
        imagem_perfeita_float.append(
            np.array(imageio.imread(DefinicoesClassificador.src_path_perfect[index]), dtype=np.float64))

    genoma = buscar_genoma()
    lista_distancias = []
    lista_genomas = []
    g_normals = []
    start_time = time.time()
    for y in range(total_img):
        prettyprint.set_text(
            "Index: {}/100 | File: {}".format(y + 2, nome[y], ))
        thread = threading.Thread(target=apply_genoma, args=(genoma, g_normals, lista_genomas,
                                                             lista_distancias, imagem_float[y],
                                                             imagem_perfeita_float[y],))
        thread.start()
    while threading.active_count() > 2:
        pass
    sorted(lowest, key=lambda x: x[0])
    low = lowest[0]

    # ploting.animate(i, low)
    # output_file.write(
    #     "Minimum: {} | Iteration: {}/{} | File: {} \n Matrix: {}\n".format(low[0], i + 1,
    #                                                                        iterations, nome[y], low[1]))
    # output_file.write("--- Final Time: {:4f} seconds ---".format(time.time() - start_time))
    # output_file.close()
    prettyprint.stop_animation()
    print("Lowest distance, ", low)

print("--- Final time: %s seconds ---" % (time.time() - start_time))
