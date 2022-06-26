''' Boolean Binary Cat Swarm Optimization

Mix-relation -> percentage of cats in tracing mode
MR

Seeking mode: in this mode, displacement occurs to nearby positions
1. Seeking memory pool - number of points to be explored -> number of clones
SMP

2. Probability muting operation.
PMO

3. Counts of dimension to change - number of dimensions (vector positions) 
to be chosen to the next possible mutation.
CDC > 1
CDC = 1 '''

import math
import numpy as np

from BBCSO import BBCSO

dimensions = 500

constants = {
    'MR': 0.6,
    'SPM': 50,
    'PMO': 0.7,
    'CDC': math.floor(dimensions/10)
}

def objective_fn(array):
    fitness = np.ndarray.sum(array)
    return fitness

bbcso = BBCSO(n_cats=500, dimensions=dimensions, 
    constants=constants, objective_fn=objective_fn)

gbest = bbcso.run(iterations=500)

print('gbest fitness:', gbest.evaluate())