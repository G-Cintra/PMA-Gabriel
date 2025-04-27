import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from statsmodels.tools.validation import array_like, PandasWrapper


def hpfilter_onesided(x, lamb=1600):
    pw = PandasWrapper(x)
    x = array_like(x, 'x', ndim=1)
    nobs = len(x)

    # Create identity matrix
    I = sparse.eye(nobs, nobs)  # noqa:E741

    # Create first difference matrix
    offsets = np.array([0, 1])  # Only need two offsets for first differences
    data = np.repeat([[-1.], [1.]], nobs, axis=1)  # First difference pattern [-1, 1]
    K = sparse.dia_matrix((data, offsets), shape=(nobs - 1, nobs))

    use_umfpack = True
    trend = spsolve(I + lamb*K.T.dot(K), x, use_umfpack=use_umfpack)

    cycle = x - trend
    return pw.wrap(cycle, append='cycle'), pw.wrap(trend, append='trend')

def hpfilter_onesided2(x, lamb=1600):
    pw = PandasWrapper(x)
    x = array_like(x, 'x', ndim=1)
    nobs = len(x)

    # Create identity matrix
    I = sparse.eye(nobs, nobs)  # noqa:E741

    # Create first difference matrix
    rows = []
    cols = []
    data = []

    for i in range(1, nobs):
        # Add the two points needed for first difference
        rows.extend([i-1, i-1])
        cols.extend([i-1, i])
        data.extend([-1., 1.])

    K = sparse.coo_matrix((data, (rows, cols)), shape=(nobs-1, nobs))

    use_umfpack = True
    trend = spsolve(I + lamb*K.T.dot(K), x, use_umfpack=use_umfpack)

    cycle = x - trend
    return pw.wrap(cycle, append='cycle'), pw.wrap(trend, append='trend')


def onesided_serial(x, lamb=1600, discard=0):
    """
    One-sided HP filter that runs the standard two-sided HP filter successively
    with each new observation.

    Parameters
    ----------
    x : array_like
        The time series to filter, 1-d.
    lamb : float
        The Hodrick-Prescott smoothing parameter.
    discard : int
        Number of initial periods to discard from the results.

    Returns
    -------
    cycle : ndarray
        The estimated cycle in the data given lamb.
    trend : ndarray
        The estimated trend in the data given lamb.
    """
    pw = PandasWrapper(x)
    x = array_like(x, 'x', ndim=1)
    nobs = len(x)
    
    # Initialize trend array
    trend = np.zeros(nobs)
    
    # For first two observations, trend equals observation
    trend[0:2] = x[0:2]
    
    # For three observations
    if nobs >= 3:
        # Build matrix A for t=3
        data = np.array([[1+lamb], [-2*lamb], [1+4*lamb], [-2*lamb], [lamb]])
        offsets = np.array([-2, -1, 0, 1, 2])
        A = sparse.dia_matrix((data, offsets), shape=(3, 3))
        trend[2] = spsolve(A, x[0:3])[2]
    
    # For four or more observations
    if nobs >= 4:
        # Preliminary calculations
        x1 = np.array([1+lamb, -2*lamb, lamb])
        x2 = np.array([-2*lamb, 1+5*lamb, -4*lamb, lamb])
        x3 = np.array([lamb, -4*lamb, 1+6*lamb, -4*lamb, lamb])
        x2rev = x2[::-1]
        x1rev = x1[::-1]
        
        # For t=4
        Ibegin = np.array([0, 0, 0, 1, 1, 1, 1])
        Jbegin = np.array([0, 1, 2, 0, 1, 2, 3])
        Xbegin = np.concatenate([x1, x2])
        Iend = np.array([2, 2, 2, 2, 3, 3, 3])
        Jend = np.array([0, 1, 2, 3, 1, 2, 3])
        Xend = np.concatenate([x2rev, x1rev])
        
        A = sparse.coo_matrix((np.concatenate([Xbegin, Xend]), 
                             (np.concatenate([Ibegin, Iend]), 
                              np.concatenate([Jbegin, Jend]))), 
                            shape=(4, 4))
        trend[3] = spsolve(A, x[0:4])[3]
        
        # For t>4
        for t in range(4, nobs):
            # Add new row and column indices
            Ibegin = np.concatenate([Ibegin, [t-2]*5])
            Jbegin = np.concatenate([Jbegin, [t-4, t-3, t-2, t-1, t]])
            Xbegin = np.concatenate([Xbegin, x3])
            
            # Advance indices for end rows
            Iend = Iend + 1
            Jend = Jend + 1
            
            # Build and solve system
            A = sparse.coo_matrix((np.concatenate([Xbegin, Xend]), 
                                 (np.concatenate([Ibegin, Iend]), 
                                  np.concatenate([Jbegin, Jend]))), 
                                shape=(t+1, t+1))
            trend[t] = spsolve(A, x[0:t+1])[t]
    
    # Calculate cycle
    cycle = x - trend
    
    # Discard initial periods if requested
    if discard > 0:
        trend = trend[discard:]
        cycle = cycle[discard:]
    
    return pw.wrap(cycle, append='cycle'), pw.wrap(trend, append='trend')


import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.linalg import spsolve

def one_sided_hp_filter_serial(y, lamb=1600, discard=0):
    """
    One-sided HP filter replication (serial version).

    Parameters:
    - y: pd.Series, list, or np.ndarray of shape (T,) or (T, n)
    - lamb: smoothing parameter (default 1600)
    - discard: number of initial observations to discard (default 0)

    Returns:
    - ycycle: np.ndarray (T-discard,) or (T-discard, n)
    - ytrend: np.ndarray (T-discard,) or (T-discard, n)
    """

    # Handle input type and shape
    if isinstance(y, (pd.Series, list)):
        y = np.asarray(y)
    if y.ndim == 1:
        y = y[:, np.newaxis]  # Convert to (T, 1)

    T, n = y.shape
    ytrend = np.zeros((T, n))

    # Precompute HP filter coefficients
    x1 = np.array([1 + lamb, -2 * lamb, lamb])
    x2 = np.array([-2 * lamb, 1 + 5 * lamb, -4 * lamb, lamb])
    x3 = np.array([lamb, -4 * lamb, 1 + 6 * lamb, -4 * lamb, lamb])
    x2rev = x2[::-1]
    x1rev = x1[::-1]

    # First two observations: no filtering
    ytrend[0, :] = y[0, :]
    ytrend[1, :] = y[1, :]

    # Third observation
    t = 2
    A = sparse.lil_matrix((3, 3))
    A[0, 0:3] = x1
    A[1, 0:3] = [-2 * lamb, 1 + 4 * lamb, -2 * lamb]
    A[2, 0:3] = x1rev
    A = A.tocsc()
    for i in range(n):
        sol = spsolve(A, y[0:t+1, i])
        ytrend[t, i] = sol[t]

    # Fourth observation
    t = 3
    Ibegin = np.array([0, 0, 0, 1, 1, 1, 1])
    Jbegin = np.array([0, 1, 2, 0, 1, 2, 3])
    Xbegin = np.concatenate((x1, x2))
    Iend = np.array([2, 2, 2, 2, 3, 3, 3])
    Jend = np.array([0, 1, 2, 3, 1, 2, 3])
    Xend = np.concatenate((x2rev, x1rev))

    I = np.concatenate((Ibegin, Iend))
    J = np.concatenate((Jbegin, Jend))
    X = np.concatenate((Xbegin, Xend))

    A = sparse.csc_matrix((X, (I, J)), shape=(4, 4))
    for i in range(n):
        sol = spsolve(A, y[0:t+1, i])
        ytrend[t, i] = sol[t]

    # From fifth observation onward
    while t < T-1:
        t += 1
        Ibegin = np.concatenate((Ibegin, np.full(5, t-2)))
        Jbegin = np.concatenate((Jbegin, np.array([t-4, t-3, t-2, t-1, t])))
        Xbegin = np.concatenate((Xbegin, x3))

        Iend += 1
        Jend += 1

        I = np.concatenate((Ibegin, Iend))
        J = np.concatenate((Jbegin, Jend))
        X = np.concatenate((Xbegin, Xend))

        A = sparse.csc_matrix((X, (I, J)), shape=(t+1, t+1))
        for i in range(n):
            sol = spsolve(A, y[0:t+1, i])
            ytrend[t, i] = sol[t]

    # Calculate cycle
    ycycle = y - ytrend

    # Discard first periods if needed
    if discard > 0:
        ytrend = ytrend[discard:, :]
        ycycle = ycycle[discard:, :]

    # Flatten if originally 1D
    if ytrend.shape[1] == 1:
        ytrend = ytrend.flatten()
        ycycle = ycycle.flatten()

    return ycycle, ytrend
