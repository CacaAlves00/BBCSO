import numpy as np

def roulette(values, fitness_values):
    max = sum([fit for fit in fitness_values])
    if max == 0.0:
        return values[np.random.choice(np.array(values))]

    selection_probs = [fit/max for fit in fitness_values]

    return values[np.random.choice(len(values), p=selection_probs)]