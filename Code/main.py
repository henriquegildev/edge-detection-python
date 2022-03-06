from datetime import datetime
import os
import random
import time
import numpy as np
import glob
import scipy.ndimage
import imageio
import threading
import gui_ed as gui
from BetaCode import prettyprint

global lock
lock = threading.Lock()
randint = random.randint
global rng
rng = np.random.default_rng()


class ClassifierDefinitions:
    """Definition of image and output paths"""
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
    # Diretorio das images resultantes do treino
    src_path_results = "./TestImages/Results/Images/"
    # Diretorio das images de resultantes do teste
    src_path_test_results = "./TestImages/Results/TestResults/Images/"
    # Diretorio do ficheiro .txt com informação relativa ao treino
    src_path_results_text = "./TestImages/Results/Text/"
    src_path_recover = "./TestImages/Recover/"


def compare_images(perfect, imperfect):
    """
    Compare Images. Função de custo, devolve a diferença entre a image perfeita e a image obtida pelo processo,
    tendo em conta o tamanho da image.

    :param perfect: np.array(np.float64)
    :param imperfect: np.array(np.float64)
    :return res: np.float64
    """
    dif = np.abs(perfect - imperfect)
    res = np.sum(dif) / dif.size
    return res


def generate_genome(operator=0):
    """
    Generate Genome. Gera um genoma baseado no operador selecionado

    :param operator: int
    :return: np.array([X,Y,Z],[0,0,0],[W,U,V])
    """
    if operator == 0:  # Sobel Operator
        return np.array([[rng.uniform(-1.1, -0.9), rng.uniform(-2.1, -1.9), rng.uniform(-1.1, -0.9)], [0, 0, 0],
                         [rng.uniform(0.9, 1.1), rng.uniform(1.9, 2.1), rng.uniform(0.9, 1.1)]])
    elif operator == 1:  # Prewitt Operator
        return np.array([[rng.uniform(-1.1, -0.9), rng.uniform(-1.1, -0.9), rng.uniform(-1.1, -0.9)], [0, 0, 0],
                         [rng.uniform(0.9, 1.1), rng.uniform(0.9, 1.1), rng.uniform(0.9, 1.1)]])


def generate_population(n, operator):
    """
    Generate Population. Cria n número de genomas.

    :param n: int
    :param operator: int
    :return: list(np.array([X,Y,Z],[0,0,0],[W,U,V]))
    """
    return [generate_genome(operator) for _ in range(n)]


def refill_population(n, population, operator):
    """
    Refil Population. Insere novos genomas na população,

    :param n: int
    :param population: list(np.array([X,Y,Z],[0,0,0],[W,U,V]))
    :param operator: int
    :return: new_pop: list(np.array([X,Y,Z],[0,0,0],[W,U,V]))
    """
    for i in range(n):
        population.append(generate_genome(operator))
    return population


def select_from_population(n: int, population: list):
    """
    Select From Population. Seleciona o top 10% da população.

    :param n: int
    :param population: list(np.array([X,Y,Z],[0,0,0],[W,U,V]))
    :return: new_pop: list(np.array([X,Y,Z],[0,0,0],[W,U,V]))
    """
    new_pop = []
    population.sort()
    new_pop_temp = population[:int(n * 0.1)]
    for i in new_pop_temp:
        new_pop.append(i[1])
    return new_pop


def crossover(population: list):
    """
    Crossover. Realiza a interseção aleatória entre dois genomas, para a uma percentagem da população.

    :param population: list(np.array([X,Y,Z],[0,0,0],[W,U,V]))
    :return: new_pop: list(np.array([X,Y,Z],[0,0,0],[W,U,V]))
    """
    combinations = {}
    new_pop = []
    index = 0
    num_cross = randint(1, 5)  # Escolher aleatoriamente um elemento da lista
    for i in population:
        combinations[index] = []
        pos = randint(0, len(population) - 1)
        try:
            if pos in combinations or population[pos] == i:
                while index in combinations[pos]:
                    pos = randint(0, len(population) - 1)
        except KeyError or ValueError as err:
            pass
        combinations[index].append(pos)
        rand = population[pos]
        # Criar listas com os valores de cima e de baixo do array g1
        g1_a, g1_b = list(i[0]), list(i[2])
        # Criar listas com os valores de cima e de baixo do array g2
        g2_a, g2_b = list(rand[0]), list(rand[2])
        new_gene1_tmp = g1_a + g1_b  # Juntar as duas listas de g1 numa nova lista
        new_gene2_tmp = g2_a + g2_b  # Juntar as duas listas de g2 numa nova lista

        new_gene1_tmp_a = new_gene2_tmp[:num_cross] + new_gene1_tmp[num_cross:]
        new_gene2_tmp_a = new_gene1_tmp[:num_cross] + new_gene2_tmp[num_cross:]

        # Adicionar os novos genes ao array dos novos genes 1
        new_gene1 = np.array([new_gene1_tmp_a[:3], [0, 0, 0], new_gene1_tmp_a[3:]])
        # Adicionar os novos genes ao array dos novos genes 2
        new_gene2 = np.array([new_gene2_tmp_a[:3], [0, 0, 0], new_gene2_tmp_a[3:]])
        # Adcionar o gene 1 ao array da nova população
        new_pop.append(new_gene1)
        # Adcionar o gene 2 ao array da nova população
        new_pop.append(new_gene2)

        index += 1
    return new_pop


def random_mutation(population: list):
    """
    Random Mutation. Realiza mutações aleatórias a elementos aleatórios.

    :param population: list(np.array([X,Y,Z],[0,0,0],[W,U,V]))
    :return: new_pop : list(np.array([X,Y,Z],[0,0,0],[W,U,V]))
    """
    # Usar 10% da população
    num_random_alter = int(len(population) * 0.1)

    # Criar um array com i aleatorios do array população - 10%
    random_population_alter = np.random.choice(
        np.arange(0, len(population)), size=num_random_alter, replace=False)

    new_pop = []
    for i in random_population_alter:
        gene = population[i]
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


def apply_genome(genome, g_normals, genome_list, distance_list, image_float, perfect_image_float):
    """Apply Genome. Aplicação do genoma à imagem, obtendo a diferença entre a imagem objetivo e a obtida.

    :param genome: np.array([X,Y,Z],[0,0,0],[W,U,V])
    :param g_normals: list
    :param genome_list: list
    :param distance_list: list
    :param image_float: np.array(np.float64) - imageio.imread result matrix
    :param perfect_image_float: np.array(np.float64) - imageio.imread result matrix
    :return: g_normals: list(float)
    :return: distance_list: list(int)
    """
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


def apply_image(population, population_results, perfect_image_float, image_float, lowest, nome, i):
    """
    Apply Image. Aplicação de cada genoma na população em cada imagem da lista.

    :param population: list(np.array([X,Y,Z],[0,0,0],[W,U,V]),...)
    :param population_results: list((minimum, np.array([X,Y,Z],[0,0,0],[W,U,V])),...)
    :param perfect_image_float: np.array(np.float64) - imageio.imread result matrix
    :param image_float: np.array(np.float64) - imageio.imread result matrix
    :param lowest: list
    :param nome: string
    :param i: int - iteration
    """
    # input : population_results, perfect_image_float,image_float,lowest,y
    # output: population_results, lowest
    distance_list = []
    genome_list = []
    g_normals = []
    # Aplicação de genome
    for genome in population:
        # Aplicação de cada genoma a cada imagem
        thread = threading.Thread(target=apply_genome, args=(genome, g_normals, genome_list,
                                                             distance_list, image_float,
                                                             perfect_image_float,))
        # Launches thread
        thread.start()
    while threading.active_count() > 2:
        pass

    minimum = min(distance_list)
    # average_val.append(minimum)
    pos = distance_list.index(minimum)

    imageio.imwrite(
        ClassifierDefinitions.src_path_results +
        '/Iteration_{}/processed_{:2f}_{}'.format(i, minimum, nome),
        g_normals[pos].astype(np.uint8))
    population_results.append([minimum, genome_list[pos]])
    lowest.append([minimum, genome_list[pos]])
    # print("Minimum: ", minimum, "\n", "Matrix: ", genome_list[pos])
    # print(" Elapsed Time: {:4f} seconds | Minimum: {}".format(time.time() - start_time, minimum))
    # print("Average Fitness: {} | Best Result: {}".format(sum(average_val) / len(average_val), minimum))


def recover(value, best_genome):
    """
    Recover. Guarda o melhor genoma obtido num ficheiro de texto.

    :param value: int - valor minimo da distância obtido pelo genoma
    :param best_genome: np.array([X,Y,Z],[0,0,0],[W,U,V]) - melhor genoma obtido durante o treino
    """
    out = open(ClassifierDefinitions.src_path_recover + "gene.txt", 'w+')
    gene = list(best_genome[0]) + list(best_genome[2])
    out.write("Distancia: {} | Media: ".format(value) + "\n")
    for i in gene:
        out.write(str(i) + "\n")
    out.close()


def get_genome():
    """
    Get Genome. Obtenção do melhor genoma obtido pelo treino, localizado no diretório "./TestImages/Recover/".
    Através do ficheiro "gene.txt"

    :return: gene : np.array([X,Y,Z],[0,0,0],[W,U,V])
    """
    input_file = open(ClassifierDefinitions.src_path_recover + "/gene.txt", 'r')
    gene_tmp = []
    next(input_file)  # Jumps to second line, since first line contains best result of operator
    for i in input_file:
        gene_tmp.append(float(i))
    gene = np.array([gene_tmp[:3], [0, 0, 0], gene_tmp[3:]])
    return gene


def training(iterations, size_of_pop, operator):
    """
    Training. Função chamada para iniciar o treino do modelo

    :param iterations: int
    :param size_of_pop: int
    :param operator: int
    """
    num_file = len(glob.glob(ClassifierDefinitions.src_path_results_text + 'results*.txt'))
    # Ficheiro .txt usado para armazenar informação relativa ao treino realizado
    output_file = open("./TestImages/Results/Text/results{}.txt".format(num_file + 1), 'w+')

    # Lista com as fotos originais
    training_list = ClassifierDefinitions.src_path_original
    minimum = "None"
    # Definição do tamanho da população e sua criação
    population = generate_population(size_of_pop, operator)
    # Formação do output do programa
    operator_name = ""
    if operator == 0:
        operator_name = "Sobel"
    elif operator == 1:
        operator_name = "Prewitt"

    output_file.write(
        "Run Begin Time: {} | Run Number: {} | Projected Iterations: {} | Size of Population: {} | Base Operator: {}\n".format(
            datetime.now(),
            num_file,
            iterations,
            size_of_pop, operator_name))

    prettyprint.start_animation()
    # Numero total de imagens a ser processadas
    num_images = len(training_list)
    image_float = []
    perfect_image = []
    perfect_image_float = []
    path_list = []
    name = []
    lowest = []

    for image_file in training_list:
        # Lista para divir o diretorio de cada ficheiro um array
        path_list.append(image_file.split('\\')) # Alterar para .split('/') se for Linux
        # Buscar o valor do array que represneta o nome do ficheiro
        name.append(path_list[-1][-1])
        index = training_list.index(image_file)
        # Leitura de imagem a processar, resultando num np.array
        # imagem_raw.append(imageio.imread(image_file))
        image_float.append(
            np.array(imageio.imread(image_file), dtype=np.float64))  # Converter data type a float64

        # Leitura de imagem perfeita, resultando num np.array
        # perfect_image.append(imageio.imread(ClassifierDefinitions.src_path_perfect[index]))
        perfect_image_float.append(
            np.array(imageio.imread(ClassifierDefinitions.src_path_perfect[index]), dtype=np.float64))

    start_time = time.time()
    for i in range(0, iterations):
        # print("New Cycle - Iteration: {}/{}".format(i + 1, iterations))
        # average_val = []
        population_results = []
        os.makedirs(ClassifierDefinitions.src_path_results +
                    'Iteration_{}'.format(i + 1), exist_ok=True)
        for y in range(num_images):
            prettyprint.set_text("Iterations: {}/{} | Index: {}/200 | File: {}".format(i + 1,
                                                                                       iterations,
                                                                                       y + 1,
                                                                                       name[
                                                                                           y],
                                                                                       ))
            apply_image(population, population_results, perfect_image_float[y], image_float[y], lowest, name[y],
                        i + 1)

        population_tmp = select_from_population(
            size_of_pop, population_results)  # 10%
        population = crossover(population_tmp)  # 10%
        pop_mutation = random_mutation(population_tmp)  # +1%
        refill_population(int(0.79 * size_of_pop), population, operator)  # 10% + 79%
        population = population + population_tmp + pop_mutation  # 89% + 1% + 10%

        sorted(lowest, key=lambda x: x[0])
        low = lowest[0]

        output_file.write(
            "Minimum: {} | Iteration: {}/{} | \n Matrix: {}\n".format(low[0], i + 1,
                                                                      iterations, low[1]))
    sorted(lowest, key=lambda x: x[0])
    low = lowest[0]
    recover(low[0], low[1])
    output_file.write(
        "--- Final Time: {:4f} seconds ---".format(time.time() - start_time))
    output_file.close()
    prettyprint.stop_animation()
    # print("--- Final time: %s seconds ---" % (time.time() - start_time))


def testing():
    """Testing. Função chamada para testar o modelo."""
    # num_file = len(glob.glob(ClassifierDefinitions.src_path_results_text + 'results*.txt'))
    test_list = ClassifierDefinitions.src_path_original_test

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
            np.array(imageio.imread(ClassifierDefinitions.src_path_perfect_test[index]), dtype=np.float64))

    genome = get_genome()
    distance_list = []
    genome_list = []
    g_normals = []
    for i in range(num_images):
        prettyprint.set_text("Index: {}/{} | File: {}".format(i + 2, num_images + 1, nome[i], ))
        thread = threading.Thread(target=apply_genome, args=(genome, g_normals, genome_list,
                                                             distance_list, image_float[i],
                                                             perfect_image_float[i],))
        thread.start()
    while threading.active_count() > 2:
        pass
    count = 0
    for img in g_normals:
        imageio.imwrite(ClassifierDefinitions.src_path_test_results + 'result_test_{}_{}'.format(distance_list[count], nome[count]), img.astype(np.uint8))
        count += 1
    low = min(distance_list)
    prettyprint.stop_animation()
    print("Lowest distance: {} | Average Distance = {}".format(low, sum(distance_list) / num_images))


def run():
    """Função que corre o programa consuante seja desejado treinar ou testar."""
    f = open("parameters.txt", "r+")
    lines = f.readlines()
    test_or_train = int(lines[3])

    if test_or_train == 1:  # Inicia Treino
        f = open("parameters.txt", "r+")
        lines = f.readlines()
        iterations, size_of_pop, operator = int(lines[0]), int(lines[1]), int(lines[2])
        f.close()
        training(iterations, size_of_pop, operator)
    if test_or_train == 2:  # Inicia Teste
        testing()
    else:
        exit(0)


if __name__ == "__main__":
    gui.start()
    run()
