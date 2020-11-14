"""
GEKKO formulation of MINLP with linear objective and non-linear constraint.
Refer to Section 1 of tex/MINLP.pdf for details.
"""

from gekko import GEKKO
import random
import pprint as pp
random.seed(3)

# setup solver
m = GEKKO(remote=False)
m.options.SOLVER = 1  # APOPT = MINLP solver
m.solver_options = ['minlp_maximum_iterations 500',
                    'minlp_max_iter_with_int_sol 500',
                    'minlp_as_nlp 0',
                    'nlp_maximum_iterations 50',
                    'minlp_branch_method 1',
                    'minlp_integer_tol 0.05',
                    'minlp_gap_tol 0.01']

num_switches = 5
num_controllers = 3
theta = 1.0

mu = [random.randint(3, 6) for _ in range(num_controllers)]
cost = [random.randint(10, 40) for _ in range(num_controllers)]


x = {(i, j): m.Var(value=0, lb=0, ub=1, integer=True)
     for i in range(num_switches) for j in range(num_controllers)}


response_time = {}
for j in range(num_controllers):
    response_time[j] = 1.0 / (mu[j] - sum([x[(i, j)]
                                           for i in range(num_switches)]))

obj_fn = sum([cost[j] * sum([x[i, j] for i in range(num_switches)])
              for j in range(num_controllers)])


m.Obj(obj_fn)

for i in range(num_switches):
    m.Equation(sum([x[(i, j)] for j in range(num_controllers)]) == 1.0)

for j in range(num_controllers):
    m.Equation(response_time[j] <= theta)

m.solve(disp=False)

print('Objective: ' + str(m.options.objfcnval))
print('Status: %s' % str(m.options.SOLVESTATUS))
print('Time: %s' % str(m.options.SOLVETIME))

if m.options.SOLVESTATUS == 1:
    for i in range(num_switches):
        for j in range(num_controllers):
            if x[i, j].value[0] == 1.0:
                print("Switch {} assigned to controller {}".format(i, j))

    try:
        queuing_response_time = {}
        traffic = {}
        for j in range(num_controllers):
            traffic[j] = sum([x[i, j].value[0] for i in range(num_switches)])
            queuing_response_time[j] = 1.0 / (mu[j] - traffic[j])

        pp.pprint(queuing_response_time)

    except ZeroDivisionError:
        print("Error")
