import numpy as np


def createH(inputFile):
    text = None
    with open(inputFile, 'r') as f:
        text = f.read()
    lines = text.splitlines()
    dimension = int(lines[0])
    H = np.zeros((dimension, dimension))
    for row, line in enumerate(lines[1:]):
        for word in line.split():
            column = int(word.split(":")[0])
            H[row, column] = int(word.split(":")[1])

    for row in range(0, dimension):
        sum = H[row, :].sum();
        for column in range(0, dimension):
            if (sum > 0):
                H[row, column] = H[row, column] / sum

    print("H:\n{}\n".format(H))
    return (H)


def createS(H):
    S = H.copy()
    dimension = H.shape[0]
    for row in range(0, dimension):
        sum = S[row, :].sum();
        for column in range(0, dimension):
            if (sum <= 0):
                S[row, column] = 1 / dimension
    print("S:\n{}\n".format(S))
    return (S)


def createG(S, alpha):
    dimension = S.shape[0]
    e = np.ones(dimension)
    G = alpha * S + (1 - alpha) * (1 / dimension) * e * e.transpose()
    print("G:\n{}\n".format(G))
    return (G)


def computePR(M, iterations):
    dimension = M.shape[0]
    pi = np.full(dimension, 1 / dimension)
    for i in range(iterations):
        print("Phi {}: {} (checksum = {})".format(i, pi, pi[:].sum()))
        pi = pi @ M
    print("Phi {}: {} (checksum = {})\n".format(iterations, pi, pi[:].sum()))


np.set_printoptions(linewidth=1000, suppress=True, precision=4)
inputFile = "/home/petr/skola/DDW/ddw-cviceni04/data/edux.txt"
alpha = 0.9
iterations = 16

H = createH(inputFile)
computePR(H, iterations)

S = createS(H)
computePR(S, iterations)

G = createG(S, alpha)
computePR(G, iterations)
