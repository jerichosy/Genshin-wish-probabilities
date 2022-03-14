import random
#from pprint import pprint  # DEBUG

FIVE_STAR_WIN_RATE = 0.75
EPITOMIZED_PATH_MAX = 2
guaranteed = False
epitomized_path_count = 0
five_star_pity = 0

featured_list = ["Mistsplitter Reforged", "Skyward Spine"]

def get_five_star():
    global guaranteed
    global epitomized_path_count

    #guaranteed = True  # debug: make sure the guaranteed flag has an effect
    #print(guaranteed, end="")  # debug

    # If we have reached the maximum number of epitomized paths, then we will get the specific 5 star chosen
    # even if we aren't guaranteed
    if epitomized_path_count == EPITOMIZED_PATH_MAX:
        epitomized_path_count = 0
        guaranteed = False  # if we were guaranteed (again, no additional effect), it counts as using it up (the next one is no longer guaranteed)
        return "Mistsplitter Reforged"

    # If guaranteed is True, then we will always get a 5 star. Otherwise, we will get a 5 star with a certain probability.
    if guaranteed or random.random() < FIVE_STAR_WIN_RATE:
        guaranteed = False

        choice = random.choice(featured_list)
        # If the 5 star is the one we want, then the epitomized path count is reset
        if choice == "Mistsplitter Reforged":
            epitomized_path_count = 0
            return choice
        # Otherwise, we will increment the epitomized path count
        else:
            epitomized_path_count += 1
            return choice

    # Lost the 75/25 chance to get a featured 5 star, so we will get a random standard 5 star weapon
    else:
        guaranteed = True  # We will get a guaranteed 5 star next time
        epitomized_path_count += 1
        return "standard 5 star wp"

def gacha():
    global five_star_pity
    gacha = random.random()
    if gacha < 0.007 or five_star_pity == 79:
        five_star_pity = 0
        return get_five_star()
    else:
        five_star_pity += 1
        return "some 3 or 4 star thingy"

history_total = []
agg_pull_history = []  # Stats

# SET NO. OF SIMULATIONS HERE (default of 10k for convenience, can be 100k for more accuracy)
for _ in range(100000):
    total_pulls = 0  # total pulls that it took to get a 5 star
    featured_5 =  {"Mistsplitter Reforged" : 0, "Skyward Spine" : 0}

    # This is True for my current situation (each simulation needs to be start with this True). If not, just comment it out.
    guaranteed = True  

    #current = []  # DEBUG

    while featured_5["Mistsplitter Reforged"] < 1:
        current_pull = gacha()
        total_pulls += 1
        if current_pull in featured_5:
            featured_5[current_pull] += 1

        #current.append(current_pull)  # DEBUG
        agg_pull_history.append(current_pull)  # Stats
        
    # DEBUG
    # if total_pulls > 240:
    #     pprint(current)
    #     exit()

    history_total.append(total_pulls) # or `history_total += [total_pull]`

print("--- RESULTS ---")
#print(history_total)
print(f"[DEBUG] Min: {min(history_total)}, Max: {max(history_total)}")
print("Avg. number of pulls required to get Mistsplitter Reforged:", sum(history_total)/len(history_total))
print("Avg. number of primogems required to get Mistsplitter Reforged:", sum(history_total)/len(history_total) * 160)


# Statistics
print("\n--- Statistics ---")
print(f"Total pulls: {len(agg_pull_history)}")
non_5_star_count = agg_pull_history.count("some 3 or 4 star thingy")
print(f"Total 5 star pulls: {len(agg_pull_history) - non_5_star_count}, Total 3 or 4 star pulls: {non_5_star_count}")
print(non_5_star_count / len(agg_pull_history) * 100, "% of the pulls were non-5 star")
print(f"{len(agg_pull_history) - non_5_star_count} / {len(agg_pull_history)} = {(len(agg_pull_history) - non_5_star_count) / len(agg_pull_history) * 100} % of the pulls were 5 star")