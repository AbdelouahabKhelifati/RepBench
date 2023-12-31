import numpy as np
from numpy import linalg as LA


# Centroid Decomposition, with the optional possibility of specifying truncation or usage of initial sign vectors
def centroid_decomposition(matrix, truncation=0, SV=None):
    # input processing
    matrix = np.asarray(matrix, dtype=np.float64).copy()
    n = len(matrix)
    m = len(matrix[0])

    if truncation == 0:
        truncation = m

    if truncation < 1 or truncation > m:
        print("[Centroid Decomposition] Error: invalid truncation parameter k=" + str(truncation))
        print("[Centroid Decomposition] Aboritng decomposition")
        return None

    if SV is None:
        SV = default_SV(n, truncation)

    if len(SV) != truncation:
        print(
            "[Centroid Decomposition] Error: provided list of Sign Vectors doesn't match in size with the truncation truncation parameter k=" + str(
                truncation))
        print("[Centroid Decomposition] Aboritng decomposition")
        return None

    L = np.zeros((truncation, n))
    R = np.zeros((truncation, m))

    # main loop - goes up till the truncation param (maximum of which is the # of columns)
    for j in range(0, truncation):
        # calculate the sign vector
        Z = local_sign_vector(matrix, SV[j])

        # calculate the column of R by X^T * Z / ||X^T * Z||
        R_i = matrix.T @ Z
        R_i = R_i / np.linalg.norm(R_i)
        R[j] = R_i

        # calculate the column of L by X * R_i
        L_i = matrix @ R_i
        L[j] = L_i

        # subtract the dimension generated by L_i and R_i from the original matrix
        matrix = matrix - np.outer(L_i, R_i)

        # update the new sign vector in the array
        SV[j] = Z
    # end for

    return (L.T, R.T, SV)


# end function


# Algorithm: LSV (Local Sign Vector). Finds locally optimal sign vector Z, i.e.:
#   Z being locally optimal means: for all Z' sign vectors s.t. Z' is one sign flip away from Z at some index j,
#   we have that ||X^T * Z|| >= ||X^T * Z'||
def local_sign_vector(matrix, Z):
    n = len(matrix)
    m = len(matrix[0])
    eps = np.finfo(np.float64).eps

    Z = local_sign_vector_init(matrix, Z)

    # calculate initial product of X^T * Z with the current version of Z
    direction = matrix.T @ Z
    # calculate initial value of ||X^T * Z||
    lastNorm = np.linalg.norm(direction) ** 2 + eps

    flipped = True

    while flipped:
        # we terminate the loop if during the last pass we didn't flip a single sign
        flipped = False

        for i in range(0, n):
            signDouble = Z[i] * 2
            gradFlip = 0.0

            # calculate how ||X^T * Z|| would change if we would change the sign at position i
            # change to the values of D = X^T * Z is calculated as D_j_new = D_j - 2 * Z_i * M_ij for all j
            for j in range(0, m):
                localMod = direction[j] - signDouble * matrix[i][j]
                gradFlip += localMod * localMod

            # if it results in augmenting ||X^T * Z||
            # flip the sign and replace cached version of X^T * Z and its norm
            if gradFlip > lastNorm:
                flipped = True
                Z[i] = Z[i] * -1
                lastNorm = gradFlip + eps

                for j in range(0, m):
                    direction[j] -= signDouble * matrix[i][j]
                # end for
            # end if
        # end for
    # end while

    return Z


# end function


# Auxiliary function for LSV:
#   Z is initialized sequentiually where at each step we see which sign would give a larger increase to ||X^T * Z||
def local_sign_vector_init(matrix, Z):
    n = len(matrix)
    m = len(matrix[0])
    direction = matrix[0]

    for i in range(1, n):
        gradPlus = 0.0
        gradMinus = 0.0

        for j in range(0, m):
            localModPlus = direction[j] + matrix[i][j]
            gradPlus += localModPlus * localModPlus
            localModMinus = direction[j] - matrix[i][j]
            gradMinus += localModMinus * localModMinus

        if gradMinus > gradPlus:
            Z[i] = -1

        for j in range(0, m):
            direction[j] += Z[i] * matrix[i][j]

    return Z


# end function


# initialize sign vector array with default values
def default_SV(n, k):
    # default sign vector is (1, 1, ..., 1)^T
    baseZ = np.array([1.0] * n)
    SV = []

    for i in range(0, k):
        SV.append(baseZ.copy())

    return SV