import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from statsmodels.tools.validation import array_like, PandasWrapper

def hpfilter_didactic(x, lamb=1600):

    pw = PandasWrapper(x)
    x = array_like(x, 'x', ndim=1)
    nobs = len(x)
    I = sparse.eye(nobs, nobs)  # noqa:E741
    offsets = np.array([0, 1, 2])
    data = np.repeat([[1.], [-2.], [1.]], nobs, axis=1)
    K = sparse.dia_matrix((data, offsets), shape=(nobs - 2, nobs))

    use_umfpack = True
    trend = spsolve(I+lamb*K.T.dot(K), x, use_umfpack=use_umfpack)

    cycle = x - trend
    return pw.wrap(cycle, append='cycle'), pw.wrap(trend, append='trend')