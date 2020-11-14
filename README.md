# optimization
Repository containing experiments and tutorials related to various optimization problems and packages.

## Installation and running the code
The easiest way is to use a conda environment. 
For instructions on getting started with the conda package manager, refer to the [conda documentation](https://docs.conda.io/projects/conda/en/latest/index.html).


Setup a conda environment by using the ```environment.yml``` file in this repository. 

    $ conda env create -f environment.yml

The environment created will be named ```cvxpy``` by default. The the command below to see the list of conda enviroments.

    $ conda info -e



You may also need to setup/configure the individual solvers. See instructions below.

# Modelling languages / frameworks

## Setting up CVXPY
- (CVXPY)[https://www.cvxpy.org/] is a Python-embedded modeling language for convex optimization problems. It allows you to express your problem in a natural way that follows the math, rather than in the restrictive standard form required by solvers.

**Important!** CVXPY is *NOT* a solver, it is a modelling language.  CVXPY relies on the open source solvers ECOS, OSQP, and SCS. It also supports other solvers such as [CVXOPT](https://cvxopt.org/) and [Gurobi](https://www.gurobi.com/) which must be installed separately.

- If you need to solve a large mixed-integer problem quickly, or if you have a nonlinear mixed-integer model, then you will need to use a commercial solver such as Gurobi.

- CVXPY should come with CVXOPT and Gurobi solvers installed when using the conda environment.

- Run ```cvxpy_example.py``` to test default cvxpy installation.
- Run ```cvxpy_solvers.py``` to test cvxpy configuration with CVXOPT and Gurobi external solvers.

## PuLP LP modelling framework

**Description**  
(PuLP)[https://coin-or.github.io/pulp/] is an LP modeler written in Python. PuLP can generate MPS or LP files and call GLPK, COIN-OR CLP/CBC, CPLEX, GUROBI, MOSEK, XPRESS, CHOCO, MIPCL, SCIP to solve **linear problems**.

**Installation**
Should be installed by default in the conda environment.

Run ```pulp_shortest_path.py``` example to test if PuLP has been configured correctly.



## GUROBI optimizer

**Description**  
[Gurobi](https://www.gurobi.com/) is a commercial optimization solver that can handle the following problem types - Linear programming (LP), Mixed-integer linear programming (MILP), Quadratic programming (QP) (Convex and Non-Convex), Mixed-integer quadratic programming (MIQP), (Convex and Non-Convex), Quadratically-constrained programming (QCP) (Convex and Non-Convex), Mixed-integer quadratically-constrained programming (MIQCP) (Convex and Non-Convex).

**Installation**

Download and install the Gurobi software. If you are using the conda environment as stated above, Gurobi will be automatically installed using conda.
Else, go to the [Gurobi website](https://www.gurobi.com/), download and install it. 

```gurobipy``` is the python API for the Gurobi software, which is automatically installed when using conda.

You need to have a Gurobi license to solve optimization problem with any reasonable number of variables. Luckily, Gurobi provides a free academic license. You need to sign up for a free account, and register for an academic license.

**Important!** Put the license key in the home directory, so that Gurobi can find it easily.

Run the ```gurobi_python_api.py``` file to test if Gurobi has been configured properly.






## GEKKO optimization package

**Description**  
[GEKKO](https://gekko.readthedocs.io/en/latest/) is a Python package for machine learning and optimization of mixed-integer and differential algebraic equations. It is coupled with large-scale solvers for linear, quadratic, nonlinear, and mixed integer programming (LP, QP, NLP, MILP, MINLP).

Capable of solving **mixed integer non-linear problems**. Solvers include APOPT, BPOPT, IPOPT. Refer to the [APMonitor documentation](https://apmonitor.com/wiki/index.php/Main/OptionApmSolver) for details.

**Installation**  
Should be installed by default if using the conda environment. Else refer to the [GEKKO documentation](https://gekko.readthedocs.io/en/latest/) for installation process.

Run the ```gekko_example.py``` file to check if GEKKO has been configured properly.

