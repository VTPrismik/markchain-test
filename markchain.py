"""
A little practice project i did for fun. Makes creating and testing markov chains easy https://en.wikipedia.org/wiki/Markov_chain 
I was originally planning to add a way to save and load chains but decided not to.
AI did none of the planning or coding, only a few bug fixes and setting suggestions. I am against using AI for most of a projects code.
I think I made this pretty efficient, doing around 2660000 iterations per second on my ryzen 5 9600x with prints off. 

Maybe later I will add support for multiple start points or multithread it.
"""
"""
Each chain is a dictionary {} with each "node" having a key and another dictionary to itself. Something like:

{
    "Example Node": { # Tabs/Line Breaks arent necessary but improve readability

    }
}

Inside of each nodes dictionary you make a tuple of each node it goes out to, along with weights equaling to exactly 1.
What 'input_chain' is set to right now is an example of a chain.
"""
import random
import time

input_chain = {
    "TestA": {
        "TestB": 0.5,
        "TestC": 0.2,
        "TestA": 0.3
    },
    "TestB": {
        "TestA": 0.2,
        "TestC": 0.8
    },
    "TestC": {
        "TestA": 0.5,
        "TestC": 0.5
    }
}
start_node = "TestA"
stop_at = "4000000"
delay = "" # time between iterations. leave blank for none

print_nodes = False # if True then each node that the script chooses will be printed. The total will still print with this False. massively increases performance when turned off
print_step = None # prints the totals and iterations of the way towards the stopping point. set to 'None' to disable. print_nodes is actually faster than this up to around 15000
pause_at_step = False # pauses at each step until enter/return key is pressed
# ------------------------------

def pick_random(chain):
    weights = list(chain.values())
    choices = list(chain.keys())

    c_weights = []
    total = 0
    for weight in weights:
        total += weight
        c_weights.append(total)

    rand_val = random.random()

    for node, weight in enumerate(c_weights):
        if rand_val < weight:
            return choices[node]
    return None

def main(chain, start, max_iterations, delay = None):
    chosen_nodes = []
    next_node = start
    iterations = 0
    if not max_iterations:
        print("There is nothing in 'stop_at'!")
        return
    try:
        max_iterations = int(max_iterations)
    except ValueError:
        print(f"'{max_iterations}' is not a valid number")
        return
    steps = 1
    while True:
        try:
            next_node = pick_random(chain[next_node])
            if print_nodes:
                print(next_node)
            chosen_nodes.append(next_node)
        except KeyboardInterrupt:
            break
        if print_step:
            next_step = steps * print_step
            if iterations == next_step:
                steps += 1
                print("---------------------------------------------------------")
                print(f"{iterations}/{max_iterations}")
                for key, data in chain.items():
                    print(f"{key}: {chosen_nodes.count(key)}")
                if pause_at_step:
                    input("Paused. Press Enter to continue")
                else:
                    print("Waiting 1 second")
                    time.sleep(1)

        iterations += 1
        if delay:
            time.sleep(delay)
        if max_iterations <= iterations:
            print(f"Reached max iterations {max_iterations}")
            break
    for key, data in chain.items():
        print(f"{key}: {chosen_nodes.count(key)}")
    print(f"Finished in {time.process_time()} seconds")

if __name__ == "__main__":
    main(input_chain, start_node, stop_at, delay)
