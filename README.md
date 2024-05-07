# Path Planning via BMC and Hyper-Properties

## Overview

The objective is to find a path on a given grid, encompassing N by N dimensions, with a central agent and multiple dynamic counteragents. The task is to ascertain a viable path for the main agent that adheres to step-by-step validity and avoids collisions with counteragents. This is achieved by transforming the grid into Kripke Structures, subsequently translated into Boolean formulas, and presented to SAT solvers. A solution to these formulas equates to a valid path for the main agent, therefore reducing the pathfinding challenge into a SAT problem. The formulas, acting as the model, undergo iterative evaluation up to a specified bound (BMC), representative of the main agent's path length.

## Features

- Design and custom grid with counter agents movements
- Auto generate a counter agent system according to parameters
- View the system as kripke structures with occupancy indicators
- Solve with timeout and bound constraints
- Iterative animation of the path found

## Documentation: Guides and Tutorial
- User Manual
- Maintenance Guide
- Demonstration Video
- Project Presentation
- Project Research Book
  
## Project Hierarchy

### Analyzer Folder
- **Test.py:** Running automated tests with specific parameters (also serves as backend code example)

### Models Folder
- **Kripke.py:** Kripke Structure representation
- **Node.py:** Node in Kripke structure representation
- **Robot.py:** A counter-agent representation
- **System.py:** A System with counter agents representation

### Services Folder
- **FileManager.py:** Imports and exports .sys files from/to the file system
- **KripkeGenerator.py:** Generates Kripke structures from Systems and auto generates systems according to given input parameters
- **Formulizer.py:** Reduces Kripke structures into SAT problem and generates a formula representing the system
- **Solver.py:** Attempts to find a suitable path for the given formula using Z3 solver and BMC

### Util Folder
- **Visual.py:** A small visual utilities function class 

### Root Folder
- **___View.py files:** The GUI layer of the system, interacting with the Services via the Models


## Installation

To install the project dependencies, run:
```
pip install -r requirements.txt
```
## Usage

Consult the User Manual supplied in the Project Book: Capstone Project Phase B-23-2-R5.docx - User Manual Section

## Code Usage Example
The following codes demonstrates a basic benchmark recorder using the Models and Services provided in this project.

```
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

```

## Contributors

- Daniel Belaish
- Liron Lavi
