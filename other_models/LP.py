import numpy as np
import  scipy.optimize as opt
import scipy.sparse as sp


#for time differences = 1 only
#time = None assume values with time differences of 1
def LPconstrainedAE(x,min = 6,max = 6 , time = None, w = 1 ,second = True):

    n = len(x)
    c = np.ones(2*n)

    t1 = np.ones(n-1)
    t2 = np.ones(n-2)
    if time is not None:
        pass



    #one difference
    A = np.zeros((n-1,n),dtype=np.byte)
    A[np.arange(n-1) ,  np.arange(n-1) ] = 1
    A[np.arange(n-1) ,  np.arange(1,n) ] = -1
    B = np.concatenate((-A,A),axis=1, )
    B = np.concatenate((B,-B),axis=0, )

    xij = x[:-1] - x[1:]
    b = np.concatenate((xij+max,-xij+min),axis=0)

    # two difference
    if second:
        A2 = np.zeros((n - 2, n), dtype=np.byte)
        A2[np.arange(n - 2), np.arange(n - 2)] = 1
        A2[np.arange(n - 2), np.arange(2, n)] = -1
        B2 = np.concatenate((-A2, A2), axis=1, )
        B2 = np.concatenate((B2, -B2), axis=0, )

        xij2 = x[:-2] - x[2:]
        b2 = np.concatenate((xij2 + max, -xij2 + min), axis=0)

        #merge one and two

        B = np.concatenate((B, B2), axis=0, )
        b = np.concatenate((b,b2))



    solution = opt.linprog(c ,method='highs',A_ub= B  , b_ub=b,bounds=(0,np.inf) , options = {"disp" : False })
    uv = solution.x
    x_prime = x+uv[:int(len(uv)/2)] - uv[int(len(uv)/2):]



    return x_prime

#print(LPconstrainedAE(np.arange(500)))
#example form the paper
x = np.array([12, 12.5, 13, 10, 15, 15.5])
t = np.array([1, 2, 3, 5, 7,8])

sol = LPconstrainedAE(x, 0.5,0.5)


paper = np.array([12.5, 13, 13.5, 14, 14.5, 15.5])


print(sum(np.abs( x-sol)))
print(sum(np.abs( x-paper )))



