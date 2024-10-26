import random
import sys
import json
import time
import initialSolution as initSol
import misc as m
import repairAndDestroy as rd
import lns as l

def read_instance_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def write_instance_json(solution, file_path):
    with open(file_path, 'w') as f:
        json.dump(solution, f)

instance_path = sys.argv[1]
output_path = sys.argv[2]

instance = read_instance_json(instance_path)
# naive_solution = [i for i in range(len(instance['Matrix']))] # TODO - implement something better

#TODO remove
# initial_solution, cost = initSol.getInitialSolution("nearest", instance['Matrix'])

# -------------------- PROGRAM LOGIC --------------------
# Get initial feasible solution

initial_solution = initSol.getInitialSolution("random", instance['Matrix'])
# print(f"Initial solution: {initial_solution} \n cost: {m.calculateCost(initial_solution, instance['Matrix'])}")


sol = initial_solution[:]

num_of_iterations = 800

solution, cost = l.lns(num_of_iterations, initial_solution, instance['Matrix'])

print(f"##########################################################################################")
print(f"Initial solution: {sol} \n") 
print(f"Found solution: {solution} \n")
print(f"Actual solution: {instance['GlobalBest']}\n\n")
print(f"Initial cost: {m.calculateCost(sol, instance['Matrix'])}\n")
print(f"Found cost: {m.calculateCost(solution, instance['Matrix'])}\n")
print(f"Actual cost: {instance['GlobalBestVal']}\n")
print(f"##########################################################################################")
# print(f"Time elapsed after generating solution: {end_time - start_time} while timeout is: {instance['Timeout']}")
print(f"Initial solution: {initial_solution} \n cost: {m.calculateCost(initial_solution, instance['Matrix'])}")
#usage of LNS

# lns = l.lns(1000, initial_solution, instance['Matrix'])
print(lns)

num_of_iterations = 200

# Write the solution into .json out
write_instance_json(initial_solution, output_path)


#######################################################################
# Example of the required timeout mechanism within the LNS structure: #
#######################################################################
# ...
# time_limit = instance['Timeout']
# start_time = time.time()
# for iteration in range(9999999999):
#     ...logic of one search iteration...
#     if time.time() - start_time >= time_limit:
#         break
# ...
#######################################################################
#######################################################################

