"""
Run this example to check if cvxpy is working properly with external solvers such as CVXOPT and Gurobi"""


import cvxpy as cp
import numpy as np

# Problem data.
m = 30
n = 20
np.random.seed(1)
A = np.random.randn(m, n)
b = np.random.randn(m)

# Construct the problem.
x = cp.Variable(n)
objective = cp.Minimize(cp.sum_squares(A@x - b))
constraints = [0 <= x, x <= 1]
prob = cp.Problem(objective, constraints)

# Solve with GUROBI.
prob.solve(solver=cp.GUROBI)
print("optimal value with GUROBI:", prob.value)

# Solve with CVXOPT.
prob.solve(solver=cp.CVXOPT)
print("optimal value with CVXOPT:", prob.value)
