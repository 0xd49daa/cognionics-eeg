import numpy as np
import matplotlib.pyplot as plt

def morlet_wavelet(srate, n_cycles, frex, width):
    time = np.arange(0, width * srate) / srate
    time = time - np.mean(time)

    s = n_cycles / (2 * np.pi * 12)

    return np.multiply(np.exp(1j * 2 * np.pi * frex * time), np.exp(np.float_power(time, 2.)/(-2 * np.float_power(s, 2.0))))
