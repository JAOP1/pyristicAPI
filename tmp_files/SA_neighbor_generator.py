import numpy as np
def neighbor_generator(x : np.ndarray) -> np.ndarray: 

    x_ = x.copy()
    N = len(x_)
    index1 = np.random.randint(1, N-1)
    index2 = np.random.randint(1, N-1)

    while index2 == index1:
        index2 = np.random.randint(1, N-1)

    v = x[index1]
    x_ = list(x_[v != x_])
    x_ = x_[:index2] + [v] + x_[index2:]
    return np.array(x_)