""" CS022B - SJSU - Project
    First implementation of all functions
    first_test.py - 25-11-2019
    Author: Kasper Meldgaard"""

# consts:
sequence_syms = {
    'a': 0, 'o': 1, 'u': 2, 'i': 3, 'e': 4, 'y': 5, 'b': 6, 'c': 7, 'd': 8, 'f': 9, 'g': 10, 'h': 11, 'j': 12,\
    'k': 13, 'l': 14, 'm': 15, 'n': 16, 'p': 17, 'q': 18, 'r': 19, 's': 20, 't': 21, 'v': 22, 'x': 23, 'z': 24, 'w': 25,\
    ' ': 26}


# import all the shit
import numpy as np
from hmm import HMM
from observation import Latin_observations
from alpha_pass_Copy_With_Changes import alpha_pass
from beta_pass import beta_pass
from log_prob import compute_logprob
from ForwardBackward import Forward_Backward

# Initialize calculation
max_iteration = 10
old_log_prob = -float('inf')
log_prob_history = np.array(old_log_prob, dtype=float)

model = HMM(2,27)
obs = Latin_observations('test_text.txt')

for iteration in range(max_iteration):
    # alpha pass
    alpha, c = alpha_pass(model, obs)

    # beta pass
    beta = beta_pass(model, obs, c)

    # gamma-pass
    start_probs, trans, emis, gamma, di_gamma = \
        Forward_Backward(model.get_N(), alpha, beta, obs.obs, sequence_syms, model.A, model.B)

    # update model
    model.A = trans
    model.B = emis

    # compute lob probs
    new_log_prob = compute_logprob(obs, c)

    # compare
    log_prob_history = np.append(log_prob_history, new_log_prob)
    if new_log_prob > old_log_prob:
        old_log_prob = new_log_prob
        continue
    else:
        break

# view some results:
print("Model:\nA:\n", model.A, "\nB:\n", model.B, "\npi:\n", model.pi)