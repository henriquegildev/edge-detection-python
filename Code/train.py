import os
import matplotlib as plt
import prettyprint
# import ploting

import prettyprint
import random
import traceback
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
    src_path = "./TestImages/Training"  # Diretorio de todas as imagens de trieno
    # Diretorio das images de treino originais
    src_path_original = glob.glob(src_path + "/*/Original/*")
    # Diretorio das images de treino perfeitas
    src_path_perfect = glob.glob(src_path + "/*/Perfect/*")
    # Diretorio das images de treino resultantes
    src_path_results = "./TestImages/Results/Images/"
    # Diretorio do ficheiro .txt com informação relativa ao treino
    src_path_results_text = "./TestImages/Results/Text/"
    src_path_recover = "./TestImages/Recover/"


"""
Função que busca todas as imagens dentro da pasta indicada
"""


def buscar_lista_de_treino(caminho):
    # print(caminho)
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


def gerar_genoma(operator=0):
    if operator == 0:  # Sobel Operator
        return np.array([[rng.uniform(-1.1, -0.9), rng.uniform(-2.1, -1.9), rng.uniform(-1.1, -0.9)], [0, 0, 0],
                         [rng.uniform(0.9, 1.1), rng.uniform(1.9, 2.1), rng.uniform(0.9, 1.1)]])
    elif operator == 1:  # Robinson Operator
        return np.array([[rng.uniform(-1.1, -0.9), rng.uniform(-1.1, -0.9), rng.uniform(-1.1, -0.9)], [0, 0, 0],
                         [rng.uniform(0.9, 1.1), rng.uniform(0.9, 1.1), rng.uniform(0.9, 1.1)]])
    elif operator == 2:  # Fri-Chen Operator
        return np.array([[rng.uniform(-1.1, -0.9), rng.uniform(-1.5, -1.3), rng.uniform(-1.1, -0.9)], [0, 0, 0],
                         [rng.uniform(0.9, 1.1), rng.uniform(1.3, 1.5), rng.uniform(0.9, 1.1)]])


"""
Nome: Gerar N Genomas;
Desc.: Chama a função gerar_genoma N vezes, devolvendo uma lista com N genomas;
Input: N -> int;
"""


def gerar_populacao(n, operator):
    return [gerar_genoma(operator) for _ in range(n)]


def encher_populacao(n, populacao, operator):
    for i in range(n):
        populacao.append(gerar_genoma(operator))
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
    # print("Old population size: {} ~ New population size: {}".format(len(populacao), len(new_pop)))
    return new_pop


"""
Nome: Crossover
Desc.: Realiza troca de genes entre os melhores 10% da populacao
Input: populacao -> list(genoma); comparar_imagens -> original_image, processed_image; original_image -> np.array(float64); processed_image -> np.array(float64)
"""


# Implementar evolucao da funcao de custo
# Crossover fazer de 1-5 com distribuicao centrada no 3
# Fazer swap fixo, mas quais sao
def crossover(populacao: list):
    combinations = {}
    new_pop = []
    index = 0
    num_cross = randint(1, 5)  # Escolher aleatoriamente um elemento da lista
    for i in populacao:
        combinations[index] = []
        pos = randint(0, len(populacao) - 1)
        try:
            if pos in combinations or pos == i:
                while index in combinations[pos]:
                    pos = randint(0, len(populacao) - 1)
        except KeyError as err:
            # print("Something happened: ", err)
            traceback.print_exc()
        combinations[index].append(pos)
        rand = populacao[pos]
        print("i:", i)
        # Criar listas com os valores de cima e de baixo do array g1
        g1_a, g1_b = list(i[0]), list(i[2])
        # Criar listas com os valores de cima e de baixo do array g2
        g2_a, g2_b = list(rand[0]), list(rand[2])
        new_gene1_tmp = g1_a + g1_b  # Juntar as duas listas de g1 numa nova lista
        new_gene2_tmp = g2_a + g2_b  # Juntar as duas listas de g2 numa nova lista

        new_gene1_tmp_a = new_gene2_tmp[:num_cross] + new_gene1_tmp[num_cross:]
        new_gene2_tmp_a = new_gene1_tmp[:num_cross] + new_gene2_tmp[num_cross:]

        # Adicionar os novos genes ao array dos novos genes 1
        new_gene1 = np.array(
            [new_gene1_tmp_a[:3], [0, 0, 0], new_gene1_tmp_a[3:]])
        # Adicionar os novos genes ao array dos novos genes 2
        new_gene2 = np.array(
            [new_gene2_tmp_a[:3], [0, 0, 0], new_gene2_tmp_a[3:]])
        # Adcionar o gene 1 ao array da nova população
        new_pop.append(new_gene1)
        # Adcionar o gene 2 ao array da nova população
        new_pop.append(new_gene2)

        index += 1
    return new_pop


"""
Nome: random_mutation
Desc.: Gera mutações aleatoriamente em 1% da população
Input: populacao -> list(genoma);
"""

# Gerar mutações aleatoriamente
# Ocorrencias que podem ser pior ou melhor


def random_mutation(populacao: list):
    # Usar 10% da população
    num_random_alter = int(len(populacao) * 0.1)

    # criar um array com i aleatorios do array população - 10%
    random_population_alter = np.random.choice(
        np.arange(0, len(populacao)), size=num_random_alter, replace=False)

    new_pop = []
    for i in random_population_alter:
        gene = populacao[i]
        g_a = list(gene[0])  # Criar uma lista com os valores de cima do array
        g_b = list(gene[2])  # Criar uma lista com os valores de baixo do array
        new_gene_tmp = g_a + g_b  # Juntar as duas listas numa nova lista
        # Escolher aleatoriamente um elemento da lista
        rnd = random.randint(0, 5)
        # Verificar se o valor se trata um da parte de cima ou da parte de baixo
        # Caso o valor for de cima os valores utilizados são positivos, caso contrario são negativos
        if rnd >= 3:
            # Verificar se o elemento escolhido aleatoriamente é 4
            if rnd == 4:
                new_gene_tmp[rnd] = rng.uniform(1.8, 2.2)
            else:
                new_gene_tmp[rnd] = rng.uniform(0.8, 1.2)
        else:
            # Verificar se o elemento escolhido aleatoriamente é 1
            if rnd == 1:
                new_gene_tmp[rnd] = rng.uniform(-2.2, -1.8)
            else:
                new_gene_tmp[rnd] = rng.uniform(-1.2, -0.8)
        new_gene = np.array([new_gene_tmp[:3], [0, 0, 0], new_gene_tmp[3:]])
        new_pop.append(new_gene)
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
Nome: apply_image
Desc.: Aplica o genoma a cada imagem
Input: populacao_results, imagem_perfeita_float, imagem_float : float, lowest : list, nome : string, i : int index
"""


def apply_image(populacao_results, imagem_perfeita_float, imagem_float, lowest, nome, i):
    # input : populacao_results, imagem_perfeita_float,imagem_float,lowest,y
    # output: populacao_results, lowest
    lista_distancias = []
    lista_genomas = []
    g_normals = []
    # Aplicação de genoma
    for genoma in populacao:
        # Associar genomas a variáveis, sendo a Y transposta
        # hX = np.array([[-1.0, -2.0, -1.0], [0, 0, 0], [1.0, 2.0, 1.0]])
        # Start thread for filter aplication
        thread = threading.Thread(target=apply_genoma, args=(genoma, g_normals, lista_genomas,
                                                             lista_distancias, imagem_float,
                                                             imagem_perfeita_float,))
        # Launches thread
        thread.start()
    while threading.active_count() > 2:
        pass

    minimum = min(lista_distancias)
    # media_val.append(minimum)
    pos = lista_distancias.index(minimum)

    imageio.imwrite(
        DefinicoesClassificador.src_path_results +
        '/Iteration_{}/processed_{:2f}_{}'.format(i, minimum, nome),
        g_normals[pos].astype(np.uint8))
    populacao_results.append([minimum, lista_genomas[pos]])
    lowest.append([minimum, lista_genomas[pos]])
    # print("Minimum: ", minimum, "\n", "Matrix: ", lista_genomas[pos])
    # print(" Elapsed Time: {:4f} seconds | Minimum: {}".format(time.time() - start_time, minimum))
    # print("Average Fitness: {} | Best Result: {}".format(sum(media_val) / len(media_val), minimum))

"""
Nome: recover
Desc.: Escreve o melhor resultado do treino para um ficheiro de texto
Input: value, best_genome, num_file
"""

def recover(value, best_genome):
    out = open(DefinicoesClassificador.src_path_recover + "gene.txt", 'w+')
    gene = list(best_genome[0]) + list(best_genome[2])
    out.write("Distance: {}".format(value) + "\n")
    for i in gene:
        out.write(str(i) + "\n")
    out.close()


def training(iterations, size_of_pop, operator):
    index = 0
    num_file = len(
        glob.glob(DefinicoesClassificador.src_path_results_text + 'results*.txt'))
    # Ficheiro .txt usado para armazenar informação relativa ao treino realizado
    #output_file = open("./TestImages/Results/Text/results.txt", 'w+')
    # Lista com as fotos originais
    lista_de_treino = DefinicoesClassificador.src_path_original
    # iterations = 10  # Número de iterações a ser realizadas
    minimum = "None"
    # Definição do tamanho da população e sua criação
    populacao = gerar_populacao(size_of_pop, operator)
    print("populacao", populacao)
    # size_of_pop = len(populacao)  # Tamanho da população
    # Formação do output do programa
    # output_file.write(
    #    "Run Begin Time: {} | Run Number: {} | Projected Iterations: {} | Size of Population: {}\n".format(
    #        datetime.now(),
    #        num_file,
    #        iterations,
    #        size_of_pop))

    prettyprint.start_animation()
    # Numero total de imagens a ser processadas
    total_img = len(lista_de_treino)
    imagem_raw = []
    imagem_float = []
    imagem_perfeita = []
    imagem_perfeita_float = []
    lista_path = []
    nome = []
    lowest = []

    for ficheiro_de_imagem in lista_de_treino:
        # Lista para divir o diretorio de cada ficheiro um array
        lista_path.append(ficheiro_de_imagem.split('\\'))
        # Buscar o valor do array que represneta o nome do ficheiro
        nome.append(lista_path[-1][-1])
        index = lista_de_treino.index(ficheiro_de_imagem)
        # Leitura de imagem a processar, resultando num np.array
        # imagem_raw.append(imageio.imread(ficheiro_de_imagem))
        imagem_float.append(
            np.array(imageio.imread(ficheiro_de_imagem), dtype=np.float64))  # Converter data type a float64

        # Leitura de imagem perfeita, resultando num np.array
        # imagem_perfeita.append(imageio.imread(DefinicoesClassificador.src_path_perfect[index]))
        imagem_perfeita_float.append(
            np.array(imageio.imread(DefinicoesClassificador.src_path_perfect[index]), dtype=np.float64))

    start_time = time.time()
    for i in range(0, iterations):
        # print("New Cycle - Iteration: {}/{}".format(i + 1, iterations))
        # media_val = []
        populacao_results = []
        os.makedirs(DefinicoesClassificador.src_path_results +
                    'Iteration_{}'.format(i + 1), exist_ok=True)
        for y in range(total_img):
            prettyprint.set_text("Iterations: {}/{} | Index: {}/200 | File: {}".format(i + 1,
                                                                                       iterations,
                                                                                       y + 1,
                                                                                       nome[
                                                                                           y],
                                                                                       ))
            apply_image(
                populacao_results, imagem_perfeita_float[y], imagem_float[y], lowest, nome[y], i + 1)

        populacao_tmp = selecionar_da_populacao(
            size_of_pop, populacao_results)  # 10%
        populacao = crossover(populacao_tmp)  # 10%
        pop_mutation = random_mutation(populacao_tmp)  # +1%
        encher_populacao(int(0.79 * size_of_pop), populacao)  # 10% + 79%
        populacao = populacao + populacao_tmp + pop_mutation  # 79% + 10% + 1%
        sorted(lowest, key=lambda x: x[0])
        low = lowest[0]

        # ploting.animate(i, low)
        #output_file.write(
        #    "Minimum: {} | Iteration: {}/{} | \n Matrix: {}\n".format(low[0], i + 1,
        #                                                              iterations, low[1]))
    sorted(lowest, key=lambda x: x[0])
    low = lowest[0]
    recover(low[0], low[1])
    #output_file.write(
    #    "--- Final Time: {:4f} seconds ---".format(time.time() - start_time))
    #output_file.close()
    prettyprint.stop_animation()

    print("--- Final time: %s seconds ---" % (time.time() - start_time))
