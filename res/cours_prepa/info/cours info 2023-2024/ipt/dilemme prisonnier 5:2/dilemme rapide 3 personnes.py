#%%

import numpy as np
import time
import random as rd
from strategies import (
    sympa_irl, bisounours, traitre, rancunnier, miroir_gentil, miroir_mechant,
    majorite, mastermind, grim_trigger, pavlov, win_stay_lose_shift,
    forgiving_tit_for_tat, suspicious_tit_for_tat, soft_majority_voting,
    generous_tit_for_tat, hard_majority_voting, adaptive, zd_extort,
    limited_retaliation, grudger, naive_prober, two_tits_for_tat, firm_but_fair,
    contrite_tit_for_tat, majorite_mechant,naive_prober2, mastermind_advanced, hacker, 
    strategie_efficace, strategie_superieure, meilleure_strategie,
    meilleure_strategie2, meilleure_strategie3, melange_strategie, strategie_opt, schema_strategie,
    strategie_amelioree, strategie_supreme
)


def print_red(text):
    print("\033[91m" + text + "\033[0m")
def print_blue(text):
    print("\033[94m" + text + "\033[0m")
def print_green(text):
    print("\033[32m" + text + "\033[0m")



def partie(N, strat1, strat2, strat3):
    L1 = np.array([], dtype=int)
    L2 = np.array([], dtype=int)
    L3 = np.array([], dtype=int)
    for _ in range(N):
        copie1 = L1.copy()
        copie2 = L2.copy()
        copie3 = L3.copy()
        if L1.size > 0:
            L1 = np.append(L1, strat1(copie2))
        else:
            L1 = np.append(L1, strat1(np.array([])))
        if L2.size > 0:
            L2 = np.append(L2, strat2(copie1))
        else:
            L2 = np.append(L2, strat2(np.array([])))
        if L3.size > 0:
            L3 = np.append(L3, strat3(copie3))
        else:
            L3 = np.append(L3, strat3(np.array([])))
    return L1, L2, L3

    

def score(arr1: np.ndarray, arr2: np.ndarray, arr3: np.ndarray):

    coop = np.logical_and(arr1, arr2, arr3)
    defect = np.logical_not(arr1) & np.logical_not(arr2) & np.logical_not(arr3)
    coop_first_coop_second_defect_third = arr1 & arr2 & np.logical_not(arr2)
    coop_first_defect_second_defect_third = arr1 & np.logical_not(arr2) & np.logical_not(arr2)
    defect_first_coop_second_coop_third = np.logical_not(arr1) & arr2 & arr3
    defect_first_coop_second_defect_third = np.logical_not(arr1) & arr2 & np.logical_not(arr3)
    coop_first_defect_second_coop_third = arr1 & np.logical_not(arr2) & arr3
    defect_first_defect_second_coop_third = np.logical_not(arr1) & np.logical_not(arr2) & arr3

    score1 = np.sum( 6*coop + 2*defect + 4*coop_first_coop_second_defect_third + 0*coop_first_defect_second_defect_third + 9*defect_first_coop_second_coop_third + 5*defect_first_coop_second_defect_third + 4*coop_first_defect_second_coop_third + 5*defect_first_defect_second_coop_third)
    score2 = np.sum( 6*coop + 2*defect + 4*coop_first_coop_second_defect_third + 5*coop_first_defect_second_defect_third + 4*defect_first_coop_second_coop_third + 0*defect_first_coop_second_defect_third + 9*coop_first_defect_second_coop_third + 5*defect_first_defect_second_coop_third)
    score3 = np.sum( 6*coop + 2*defect + 9*coop_first_coop_second_defect_third + 5*coop_first_defect_second_defect_third + 4*defect_first_coop_second_coop_third + 5*defect_first_coop_second_defect_third + 4*coop_first_defect_second_coop_third + 0*defect_first_defect_second_coop_third)

    return score1, score2, score3



def tournoi(T, P, C, D, strats: tuple):
    scores = {}
    total_scores = {}
    n = rd.randint(500, 1000)
    print(n)
    for i in range(len(strats)):
        print("\n")
        for j in range(i + 1, len(strats)):
            L1, L2 = partie(n, strats[i], strats[j])
            score1, score2 = score(T, P, C, D, L1, L2)
            
            result_str = f"{strats[i].__name__} : {score1} vs. {strats[j].__name__} : {score2}"
            print(result_str)
            
            if strats[i] not in total_scores:
                total_scores[strats[i]] = score1
            else:
                total_scores[strats[i]] += score1
            if strats[j] not in total_scores:
                total_scores[strats[j]] = score2
            else:
                total_scores[strats[j]] += score2


            if strats[i] not in scores:
                scores[strats[i]] = [(score1, strats[j])]
            else:
                scores[strats[i]].append((score1, strats[j]))
                scores[strats[i]] = scores[strats[i]][-3:]  

            if strats[j] not in scores:
                scores[strats[j]] = [(score2, strats[i])]
            else:
                scores[strats[j]].append((score2, strats[i]))
                scores[strats[j]] = scores[strats[j]][-3:]  
    
    max_total_score = max(total_scores.values())
    min_total_score = min(total_scores.values())
    for strat, total_score in total_scores.items():
        total_str = f"{strat.__name__} : {total_score} "
        if total_score == max_total_score:
            print_red(total_str + "\n")
        elif total_score == min_total_score:
            print_blue(total_str + "\n")
        elif total_score >= max_total_score - 1000:
            print_green(total_str + "\n")
        else:
            print(total_str + "\n")

    return scores, total_scores


#L1, L2 = partie(560, miroir_gentil, miroir_mechant)
#L1, L2 = partie(5, mastermind, majorite)
#print(L1, L2)
#score1, score2 = score(T, P, C, D, L1, L2)
#print(score1, score2)

start = time.time()
scores, total_score = tournoi((mastermind_advanced, strategie_efficace, strategie_superieure))
end = time.time()
print("\n", end - start)

# meilleur strat mastermind_advanced / strategie_efficace / strategie_superieur
#%%
