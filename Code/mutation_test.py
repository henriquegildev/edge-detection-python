import numpy as np
rng = np.random.default_rng()

"""
Nome: Gerar Genoma
Desc.: Gera genomas aleatórios
Input: None
Returns: 
"""

def gerar_genoma():
    return np.array([[rng.uniform(-1.1, -0.9), rng.uniform(-2.1, -1.9), rng.uniform(-1.1, -0.9)], [0, 0, 0],
                     [rng.uniform(0.9, 1.1), rng.uniform(1.9, 2.1), rng.uniform(0.9, 1.1)]])


"""
Nome: Gerar N Genomas;
Desc.: Chama a função gerar_genoma N vezes, devolvendo uma lista com N genomas;
Input: N -> int;
"""


def gerar_populacao(n):
    return [gerar_genoma() for _ in range(n)]


def randomMutation(populacao: list):
    # Ver o tamanho da população
    num_random_alter = int(len(populacao)*0.1)

    # criar um array com i aleatorios do array população - 10%
    random_population_alter = np.random.choice(np.arange(0, len(populacao)), size=num_random_alter, replace=False)

    new_pop = []
    for i in random_population_alter:
        gene = populacao[i]
        g_a = list(gene[0])
        g_b = list(gene[2])
        new_gene_tmp = g_a + g_b
        print("new_gene_tmp - ", i, new_gene_tmp)
        rnd = np.random.choice([0, 1, 2, 3, 4, 5])
        if rnd >= 3:
            if rnd == 4:
                new_gene_tmp[rnd] = rng.uniform(1.8, 2.2)
            else:
                new_gene_tmp[rnd] = rng.uniform(0.8, 1.2)
        else:
            if rnd == 1:
                new_gene_tmp[rnd] = rng.uniform(-2.2, -1.8)
            else:
                new_gene_tmp[rnd] = rng.uniform(-1.2, -0.8)
        new_gene = np.array([new_gene_tmp[:3], [0, 0, 0], new_gene_tmp[3:]])
        new_pop.append(new_gene)


