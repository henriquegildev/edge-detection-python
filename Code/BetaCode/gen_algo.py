from random import choices

import numpy as np

"""
Initial Population->Calculate Fitness->Selection->Crossover->Mutation
"""

# Genome will be two kernels, starting with a 3x3 matrix
# Initial Values

kernel1 = np.zeros(shape=(3, 3))
kernel2 = np.zeros(shape=(3, 3))
Genome = [kernel1, kernel2]

# Population is a list of Genomes
Population = [Genome]


def generate_genome(length: int) -> Genome:
    # First Kernel - Vertical
    kernel1[0, 0] = choices([0, 2])
    kernel1[0, 1] = choices([0, 2])
    kernel1[0, 2] = choices([0, 2])
    kernel1[1, 0] = 0  # Empty line
    kernel1[1, 1] = 0  # Empty line
    kernel1[1, 2] = 0  # Empty line
    kernel1[2, 0] = choices([0, -2])
    kernel1[2, 1] = choices([0, -2])
    kernel1[2, 2] = choices([0, -2])

    # Second Kernel - Horizontal
    kernel2[0, 0] = choices([0, 2])
    kernel2[0, 1] = 0  # Empty line
    kernel2[0, 2] = choices([0, -2])
    kernel2[1, 0] = choices([0, 2])
    kernel2[1, 1] = 0  # Empty line
    kernel2[1, 2] = choices([0, -2])
    kernel2[2, 0] = choices([0, 2])
    kernel2[2, 1] = 0  # Empty line
    kernel2[2, 2] = choices([0, -2])
    return [kernel1, kernel2]
