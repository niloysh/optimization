# optimization
Repository containing experiments and tutorials related to various optimization problems and packages

## Installation and running the code
The easiest way is to use a conda environment. 
For instructions on getting started with the conda package manager, refer to the [conda documentation](https://docs.conda.io/projects/conda/en/latest/index.html).


Setup a conda environment by using the ```environment.yml``` file in this repository. 

    $ conda env create -f environment.yml

The environment created will be named ```cvxpy``` by default. The the command below to see the list of conda enviroments.

    $ conda info -e



You may also need to setup/configure the individual solvers. See instructions below.

## Setting up the Gurobi solver
- Download and install the Gurobi software. If you are using the conda environment as stated above, Gurobi will be automatically installed using conda.
Else, go to the [Gurobi website](https://www.gurobi.com/), download and install it.

- ```gurobipy``` is the python API for the Gurobi software, which is automatically installed when using conda.

- You need to have a Gurobi license to solve optimization problem with any reasonable number of variables. Luckily, Gurobi provides a free academic license. You need to sign up for a free account, and register for an academic license.

**Important!** Put the license key in the home directory, so that Gurobi can find it easily.

- Run the ```gurobi_python_api.py``` file to test if Gurobi has been configured properly.


## Setting up the CVXOPT solver
- The cvxopt solver should be installed by default when using the conda environment.
- ```cvxpy``` is the python API for the cvxopt solver
