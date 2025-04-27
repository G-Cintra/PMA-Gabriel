import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def hpfilter_onesided_kalman(x, lamb=1600, discard=0):
    """
    One-sided Hodrick-Prescott filter using Kalman filter approach.
    
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
    # Convert input to numpy array if it's not already
    x = np.array(x)
    nobs = len(x)
    
    # Kalman filter parameters
    q = 1.0 / lamb  # signal-to-noise ratio
    F = np.array([[2, -1], [1, 0]])  # state transition matrix
    H = np.array([[1, 0]])  # observation matrix
    Q = np.array([[q, 0], [0, 0]])  # state error covariance
    R = np.array([[1.0]])  # observation error variance
    
    # Initialize state estimate and covariance
    x_state = np.array([2*x[0] - x[1], 3*x[0] - 2*x[1]])  # initial state estimate
    P = np.array([[1e5, 0], [0, 1e5]])  # initial state covariance
    
    # Storage for results
    trend = np.zeros(nobs)
    
    # Kalman filter recursion
    for t in range(nobs):
        # Prediction step
        x_pred = F @ x_state
        P_pred = F @ P @ F.T + Q
        
        # Update step
        S = H @ P_pred @ H.T + R
        K = (F @ P_pred @ H.T) @ np.linalg.inv(S)  # Kalman gain
        x_state = F @ x_state + K @ (x[t] - H @ x_state)
        P = (F - K @ H) @ P_pred @ (F - K @ H).T + Q + K @ R @ K.T
        
        # Store trend estimate (second element of state)
        trend[t] = x_state[1]
    
    # Calculate cycle as residual
    cycle = x - trend
    
    # Discard initial periods if requested
    if discard > 0:
        trend = trend[discard:]
        cycle = cycle[discard:]
        x = x[discard:]
    
    return cycle, trend

# Example usage
if __name__ == "__main__":
    # Create a sample time series
    t = np.linspace(0, 10, 100)
    x = np.sin(t) + 0.5*t + np.random.normal(0, 0.1, 100)
    
    # Apply the filter
    cycle, trend = hpfilter_onesided(x)