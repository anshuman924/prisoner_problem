# LOGIC
# AIM : to plot two curves (x axis : number of people surviving 1 to 100, y axis : percentage of that number happening - no strat vs strat)
# game : we have 100 boxes each numbered, each having a a number written on paper from 1-100. 100 prisoners go one by one, each opening at most 50 boxes, if they find their own number, they have a success else failure. we need to plot probabilities of x number of prisoners getting success. with and without strat
# STRAT : for each person that goes in, goto box of your own number, then next to whatever number is inside that box, and so on.

import matplotlib.pyplot as plt
import numpy as np
import logging
import coloredlogs
from concurrent.futures import ThreadPoolExecutor
import random

SIMULS = 100000
LOGGING = logging.INFO

with open('app.log', 'w'):
    pass

logging.basicConfig(
    filename='app.log',  # Name of the log file
    level=LOGGING,
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
)

logger = logging.getLogger("DEBUGGER PRO MAXX")

logging.getLogger('matplotlib').handlers = [logging.NullHandler()]
logging.getLogger('matplotlib').propagate = False

# wo_strat : list of size 100 - each having probability of i susccesses
# w_strat : list of size 100 - each having probability of i susccesses with strat
def plot_two_arrays(w_strat, wo_strat, x_values=None, labels=("wo_strat", "w_strat"), title="Plot of wo_strat and w_strat"):
    if x_values is None:
        x_values = range(len(wo_strat))  # Default to indices if x_values not provided

    fig = plt.figure(figsize=(10, 6))
    fig.canvas.manager.set_window_title(title)  # Set the figure window title

    # Plotting bar charts
    width = 0.35  # Width of the bars
    bars1 = plt.bar(x_values, wo_strat, width=width, label=labels[0], color='red', align='center')
    bars2 = plt.bar(np.array(x_values) + width, w_strat, width=width, label=labels[1], color='green', align='center')

    plt.xlabel('Number of People Survived')
    plt.ylabel('Probability of Number of People Survived')
    plt.title(title)

    # Add the values on top of the bars
    # for bar in bars1:
    #     height = bar.get_height()
    #     plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')  # va: vertical alignment
    # for bar in bars2:
    #     height = bar.get_height()
    #     plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')

    # Set x-axis ticks to show 0, 5, 10, 15, ...
    plt.xticks(np.arange(0, len(wo_strat), 5))  # Set the step size of x-axis ticks to 5

    plt.legend()
    plt.grid(True, axis='y')
    plt.show()

# with strat - for 1 to 100, goto room, choose box, reads number goes to nex box, does till box number 50, if at any point your number is there, Sucess else F

def follow_chain(room, box, prisoner, chances):
    if chances == 0:
        return False
    
    if(room[box-1] == prisoner):
        return True
    
    return follow_chain(room, room[box-1], prisoner, chances-1)

def goto_room_strat(room, prisoner):
    return follow_chain(room, prisoner, prisoner, 50)


def strat(room):
    success = 0
    for i in range(1, 101):
        if goto_room_strat(room, i):
            success += 1

    logger.info(f"strat gives {success} successes")
    return success



# without strat - for 1 to 100, goto room, choose 50 boxes at random, if any has your number, success else F
def goto_room_no_strat(room, prisoner):
    boxes_chosen = random.sample(range(1, 101), 50)

    logger.debug(f"boxes : {boxes_chosen}")
    for j in boxes_chosen:
        logger.debug(f"{room[j-1]} {prisoner}")
        if room[j-1] == prisoner:
            return True
        
    return False

def no_strat(room):
    success = 0
    for i in range(1, 101):
        if goto_room_no_strat(room, i):
            success += 1

    logger.info(f"no_strat gives {success} successes")
    return success

# General Setting : will be doing 10000 simulations of games, each with start and no strat. where each simulation gives number of sucessful ppl.

def generate_room():
    # Create an array with values from 1 to 100
    v = np.arange(1, 101)
    # Shuffle the array to randomize the order
    np.random.shuffle(v)

    logger.debug(f"room is : {np.array2string(v)}")
    return v


# n : number of simuls
# for number of simuls it increments the count arrays by 1 indicating ith entry has v[i] success. end of it divides by n for probability

def simulate_single_iteration(strat_res, no_strat_res, i):
    logger.info(f"At Simul : {i}")
    v = generate_room()
    strat_res[strat(v)] += 1
    no_strat_res[no_strat(v)] += 1


def simulate(n):
    strat_res = np.zeros(101)
    no_strat_res = np.zeros(101)

    for i in range(n):
        if i % 100 == 0:
            print(f"At Simul: {i}")
        simulate_single_iteration(strat_res, no_strat_res, i)
    
    #  # Create a thread pool with ThreadPoolExecutor
    # with ThreadPoolExecutor(max_workers=n) as executor:
    #     # Execute the simulation for each iteration in a separate thread
    #     for i in range(n):
    #         executor.submit(simulate_single_iteration, strat_res, no_strat_res, i)
    
    strat_res = strat_res/n
    no_strat_res = no_strat_res/n

    return strat_res, no_strat_res


def get_expected_value(v):
    avg = 0
    for i in range(len(v)):
        avg += i*v[i]

    return avg

strat_res, no_strat_res = simulate(SIMULS)

logger.info(f"""final probabs :
            strat :  {np.array2string(strat_res)}
            no_strat : {np.array2string(no_strat_res)}""")
logger.info(f"""avg values : 
            strat : {get_expected_value(strat_res)}
            no_strat : {get_expected_value(no_strat_res)}""")
plot_two_arrays(strat_res, no_strat_res)
