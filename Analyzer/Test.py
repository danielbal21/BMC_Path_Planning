import time
from datetime import datetime
import os
from z3 import sat
import csv

# Importing custom modules
from Services.FileManager import system_to_file
from Services.KripkeGenerator import auto_generate_system
from Services.Solver import Solve

# Define header for the CSV file
header = ['Number', 'Iterations', 'Gen Time', 'Solution Time', 'Avg Iter Time']

# Define the number of test iterations to perform
num_tests_to_perform = 2

# Define parameters for the system and solving
n = 40
counter_agents = 1
stay_chance = 0.0
stray_radius = 10
k = (2 * n) - 1
max_iter = 110  # n * n

# Generate a unique filename based on parameters
filename = f"test_n{n}_nc{counter_agents}_sr{stray_radius}_sc{int(stay_chance * 100)}_maxit{max_iter}"

# Define the path for storing test results
path = f'tests/{filename}'

# Create the directory if it doesn't exist
try:
    os.makedirs(path)
except:
    pass

# Open a CSV file for writing the results
file = open(f'{path}/{datetime.now().date()}.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)
writer.writerow(header)

# Loop through the test iterations
t = 0
while t < num_tests_to_perform:
    k = (2 * n) - 1
    start_gen = time.time()
    # Generate the system
    sys, m2 = auto_generate_system(n, counter_agents, stay_chance, stray_radius)
    end_gen = time.time()

    stat = None
    start_solve = time.time()
    # Solve the system with incremental k values until satisfiable or max_iter reached (BMC)
    while stat != sat and k <= max_iter:
        stat, sol = Solve(n, m2, k)
        if stat != sat:
            k += 1
    end_solve = time.time()

    # If satisfiable, record the results
    if stat == sat:
        t += 1
        gen_time = end_gen - start_gen
        solve_time = end_solve - start_solve
        num_iters = k - (2 * n) + 2

        # Write data to CSV
        data = [t, num_iters, gen_time, solve_time, float(solve_time) / float(num_iters)]
        writer.writerow(data)

        # Save the system to a file
        system_to_file(f'{path}/{t}.sys', m2)

        # Print results
        print(f'Generation time: {gen_time}')
        print(f'Solution time: {solve_time}')
        print(f'Iterations : {num_iters}')
        print(f'Avg Iteration Time : {float(solve_time) / float(num_iters)}')
