"""
The warehouse location problem
Modeled using PuLP
"""

import pulp
import numpy as np
from functools import wraps
from time import time


def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print('Elapsed time: {}'.format(end-start))
        return result
    return wrapper


N = 5  # warehouses
M = 8  # customers

c = np.random.uniform(low=1.0, high=10.0, size=(N, M))
f = np.random.uniform(low=30.0, high=100.0, size=(N,))
a = np.random.uniform(low=5.0, high=10.0, size=(M,))
b = np.random.uniform(low=50.0, high=70.0, size=(M,))
l = np.zeros(shape=(N, ))


@timing
def primal():
    # prob
    prob = pulp.LpProblem("Warehouse", pulp.LpMinimize)

    # variables
    x = {(i, j): pulp.LpVariable('x_%s,%s' % (i, j), cat=pulp.LpBinary)
         for i in range(N) for j in range(M)}
    y = {i: pulp.LpVariable('y_%s' % i, cat=pulp.LpBinary) for i in range(N)}

    # objective
    prob += pulp.lpSum([f[i] * y[i] for i in range(N)]) \
        + pulp.lpSum([c[(i, j)] * x[(i, j)]
                      for i in range(N) for j in range(M)])

    # constraints
    for i in range(N):
        prob += pulp.lpSum([a[j] * x[(i, j)] for j in range(M)]) <= b[i]

    for j in range(M):
        prob += pulp.lpSum([x[(i, j)] for i in range(N)]) == 1

    for i in range(N):
        for j in range(M):
            prob += x[(i, j)] <= y[i]

    # solve
    prob.solve()

    # print results
    print("Primal Status = {}".format(pulp.LpStatus[prob.status]))
    print("Objective (Primal) = {}".format(pulp.value(prob.objective)))

    return prob, pulp.value(prob.objective)


@timing
def lagrangian():
    # prob
    prob = pulp.LpProblem("Warehouse", pulp.LpMinimize)

    # variables
    x = {(i, j): pulp.LpVariable('x_%s,%s' % (i, j), cat=pulp.LpBinary)
         for i in range(N) for j in range(M)}
    y = {i: pulp.LpVariable('y_%s' % i, cat=pulp.LpBinary) for i in range(N)}

    # objective
    prob += pulp.lpSum([f[i] * y[i] for i in range(N)]) \
        + pulp.lpSum([(c[(i, j)] + l[i] * a[j]) * x[(i, j)] for i in range(N) for j in range(M)]) \
        - pulp.lpSum([l[i] * b[i] for i in range(N)])

    # constraints
    for j in range(M):
        prob += pulp.lpSum([x[(i, j)] for i in range(N)]) == 1

    for i in range(N):
        for j in range(M):
            prob += x[(i, j)] <= y[i]

    # solve
    prob.solve()

    # print results
    print("Lagrangian Status = {}".format(pulp.LpStatus[prob.status]))
    print("Objective (Lagrangian) = {}".format(pulp.value(prob.objective)))

    x_opt = {var.name: var.value() for var in x.values()}
    y_opt = {var.name: var.value() for var in y.values()}

    return x_opt, y_opt, pulp.value(prob.objective)


if __name__ == "__main__":
    primal, p = primal()
    x_opt, y_opt, l = lagrangian()
    print("Duality gap = {}".format(p - l))
    primal.assignVarsVals(x_opt)
    primal.assignVarsVals(y_opt)
    print("Primal feasible = {}".format(primal.valid()))
