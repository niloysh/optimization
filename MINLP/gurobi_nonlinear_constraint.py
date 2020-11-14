"""
Gurobi formulation of MINLP with linear objective and non-linear constraint.
Refer to Section 1 of tex/MINLP.pdf for details.

Linearize non-linear constraint using piece-wise linear function using SOS2 variables in Gurobi
For details, please refer to gurobi_piecewise_linear_constraint.png
"""


import gurobipy as gp
import numpy as np
from gurobipy import GRB, quicksum
import random
import pprint as pp
random.seed(3)

num_switches = 5
num_controllers = 3
theta = 1.0
mu = [random.randint(3, 6) for _ in range(num_controllers)]
cost = [random.randint(10, 40) for _ in range(num_controllers)]

num_samples = 100


def response_time(u, j):
    """ response time for M/M/1 queuing system """
    return 1.0 / (mu[j] - u)


# create breakpoints for non-linear functions
x_samples = {}
y_samples = {}
for j in range(num_controllers):
    x_low = 0
    x_high = 0.95 * mu[j]
    x_samples[j] = np.linspace(x_low, x_high, num_samples)
    y_samples[j] = response_time(x_samples[j], j)


try:
    m = gp.Model("Queuing_pwl")
    x = m.addVars(num_switches, num_controllers, vtype=GRB.BINARY, name="x")
    y = m.addVars(num_controllers, vtype=GRB.CONTINUOUS, name="y")

    w = m.addVars(num_samples, num_controllers, lb=0,
                  ub=1, vtype=GRB.CONTINUOUS, name="w")

    w_sum = {}
    sos2 = {}
    for j in range(num_controllers):
        sos2[j] = m.addSOS(GRB.SOS_TYPE2, w.select('*', j))
        w_sum[j] = m.addConstr(quicksum([w[i, j]
                                         for i in range(num_samples)]) == 1)

    x_link = {}
    y_link = {}
    for j in range(num_controllers):
        x_link[j] = m.addConstr(quicksum(
            [w[i, j] * x_samples[j][i] for i in range(num_samples)]) == x.sum('*', j))
        y_link[j] = m.addConstr(
            quicksum([w[i, j] * y_samples[j][i] for i in range(num_samples)]) == y[j])

    m.addConstrs((x.sum(i, '*') == 1 for i in range(num_switches)), "c1")
    m.addConstrs((y[j] <= theta for j in range(num_controllers)), "c3")

    obj_fn_1 = sum([cost[j] * sum([x[i, j] for i in range(num_switches)])
                    for j in range(num_controllers)])
    m.setObjective(obj_fn_1, GRB.MINIMIZE)

    m.optimize()

    if m.status == GRB.OPTIMAL:
        sol = m.getAttr('x', x)
        for i in range(num_switches):
            for j in range(num_controllers):
                if sol[i, j] == 1.0:
                    print("Switch {} assigned to controller {}".format(i, j))

        print("Objective = {}".format(m.objVal))

        try:
            queuing_delays = {}
            traffic = {}
            for j in range(num_controllers):
                traffic[j] = sum([sol[i, j] for i in range(num_switches)])
                queuing_delays[j] = 1.0 / (mu[j] - traffic[j])

            pp.pprint(queuing_delays)

        except ZeroDivisionError:
            print("Error")


except AttributeError:
    print("Encountered attribute error")
