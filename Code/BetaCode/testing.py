import numpy as np

def buscar_genoma(num_file):
    input_file = open("./TestImages/Recover/" + "gene{}.txt".format(num_file), 'r')
    gene_tmp = []
    next(input_file) # Jumps to second line, since first line contains best result of operator
    for i in input_file:
        gene_tmp.append(float(i))
    gene = np.array([gene_tmp[:3], [0, 0, 0], gene_tmp[3:]])
    return gene

buscar_genoma(0)