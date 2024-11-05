#%%

import numpy as np
import random as rd



def mastermind_advanced(adversaire: np.ndarray):
    if adversaire.size == 0:
        return 0
    elif adversaire.size == 1 or adversaire.size == 2:
        return 1
    elif np.all(adversaire[:3] == 1):
        return 0
    else:
        pattern = np.array([1, 0, 1])  
        history_size = len(adversaire)
        for i in range(history_size - 3):
            if np.all(adversaire[i:i+3] == pattern):
                return 1 

        return adversaire[-1]
    


def strategie_efficace(adversaire: np.ndarray):
    if adversaire.size == 0:
        return 0
    elif adversaire.size <= 2:
        return 1
    elif np.all(adversaire[:3] == 1):
        return 0
    else:
        pattern1 = np.array([1, 0, 1])
        pattern2 = np.array([0, 1, 0])
        history_size = len(adversaire)
        for i in range(history_size - 3):
            if np.all(adversaire[i:i+3] == pattern1) or np.all(adversaire[i:i+3] == pattern2):
                return 1 

        return adversaire[-1]



def strategie_superieure(adversaire: np.ndarray):
    if adversaire.size == 0:
        return 0
    elif adversaire.size <= 2:
        return 1
    elif np.all(adversaire[:3] == 1):
        return 0
    else:
        pattern1 = np.array([1, 0, 1])
        pattern2 = np.array([0, 1, 0])
        history_size = len(adversaire)
        for i in range(history_size - 3):
            if np.all(adversaire[i:i+3] == pattern1) or np.all(adversaire[i:i+3] == pattern2):
                return 1 

        return np.random.choice([0, 1])



#%%



def strategie_3_people(adversaire1 : np.ndarray, adversaire2 : np.ndarray, memoire : np.ndarray):
    

