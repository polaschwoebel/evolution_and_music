import numpy as np
from sklearn.decomposition import PCA


def fit_pca(population):
    all_chromosomes = np.array([individual.chromosome for individual in population])
    pca = PCA(n_components=5)
    reduced_chromosomes = pca.fit_transform(all_chromosomes)
    best2 = reduced_chromosomes[:2, :]
    index1 = np.argmax(best2[0, :])
    index2 = np.argmax(best2[1, :])
    return pca, [index1, index2]


def pca_fitness(individual, pca, indices):
    transformed = pca.transform(np.array(individual.chromosome).reshape((1,-1)))[0]
    print(transformed)
    fitness = transformed[indices[0]] + transformed[indices[1]]
    return fitness
