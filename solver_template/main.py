import random
import sys
import json
import time
import initialSolution as initSol
import misc as m
import lns as l

def read_instance_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def write_instance_json(solution, file_path):
    with open(file_path, 'w') as f:
        json.dump(solution, f)

# Testing variables
instance_path = sys.argv[1]
output_path = sys.argv[2]

instance = read_instance_json(instance_path)

# -------------------- PROGRAM LOGIC --------------------
start_time = time.time()

# Testing runs
initial_solution = initSol.getInitialSolution("Farthest", instance['Matrix'])


sol = initial_solution[:] 
num_of_iterations = 1000

solution, cost = l.lns(num_of_iterations, initial_solution, instance['Matrix'],instance['Timeout'],120,start_time)

# func_cost = m.calculateCost(solution, instance['Matrix']) 
# if cost != func_cost:
#     print(f"The cost returned{cost} and actual cost{func_cost} are different:")

# print(f"\n Testing of k-swap parameter with different initial solutions(1000 iterations): \n k-swap: {T_swap_cnt}, init_solution: {T_init_sol}")
print(f"#######################################################################################")
print(f"Initial solution: {sol} \n") 
print(f"Found solution: {solution} \n")
print(f"Actual solution: {instance['GlobalBest']}\n\n")
print(f"Initial cost: {m.calculateCost(sol, instance['Matrix'])}\n")
print(f"Found cost: {m.calculateCost(solution, instance['Matrix'])}\n")
print(f"Actual cost: {instance['GlobalBestVal']}\n")
print(f"#######################################################################################")
print(f"Elapsed time: {time.time()-start_time} while timeout is: {instance['Timeout'], }")

# Write the solution into .json out
write_instance_json(solution, output_path)


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

