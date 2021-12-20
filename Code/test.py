import numpy as np
import glob
import scipy.ndimage
import imageio

class DefinicoesClassificador:
    src_path_original = "C:/GitHub/edge-detection-python/Code/TestImages/Training/1-25/Original/"
    src_path_perfect = "C:/GitHub/edge-detection-python/Code/TestImages/Training/1-25/Perfect/"
    src_path_results = "C:/GitHub/edge-detection-python/Code/TestImages/Results/Images/"
    src_path_results_text = "C:/GitHub/edge-detection-python/Code/TestImages/Results/Text/"

"""
Função que busca todas as imagens dentro da pasta indicada
"""
def buscar_lista_de_treino(caminho):
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


if __name__ == '__main__':
    photos_path = "C:/GitHub/edge-detection-python/Code/TestImages/Training"
    original_photos_path = glob.glob(photos_path + "/*/Original/*")
    perfect_photos_path = glob.glob(photos_path + "/*/Perfect/*")
    print("Original Photos Paths: ", original_photos_path)
    print("Perfect Photos Paths: ", perfect_photos_path)

    lista_de_treino = buscar_lista_de_treino(DefinicoesClassificador.src_path_original)
    for ficheiro_de_imagem in lista_de_treino:
        # Leitura de imagem, resultando num np.array
        imagem = imageio.imread(ficheiro_de_imagem)

        lista_path = ficheiro_de_imagem.split('\\')
        nome = lista_path[-1]
        imagem_perfeita = imageio.imread(DefinicoesClassificador.src_path_perfect + nome)
        imagem_perfeita_float = np.array(imagem_perfeita, dtype=np.float64)
        imagem_float = np.array(imagem, dtype=np.float64)
        hX = np.array([[-1.0, -2.0, -1.0], [0, 0, 0], [1.0, 2.0, 1.0]])
        hY = np.transpose(hX)
        gX = scipy.ndimage.convolve(imagem_float, hX)
        gY = scipy.ndimage.convolve(imagem_float, hY)
        g = np.abs(gX + gY)

        g_normal = g * (255.0 / (scipy.ndimage.maximum(g) - scipy.ndimage.minimum(g)))

        distancia = comparar_imagens(imagem_perfeita_float, g_normal)
        # print(scipy.ndimage.minimum(g_normal), scipy.ndimage.maximum(g_normal))
        imageio.imwrite(DefinicoesClassificador.src_path_results + 'processed_{}'.format(nome),
                        g_normal.astype(np.uint8))
        print(nome, "| distancia: ", distancia)
        # print(imagem.shape)