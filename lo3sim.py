import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def gen_ez_2dist(numSim, entries):
    """
    Generates pandas dataframe of number of draws (labeled with number of entries/bets)

    numSim(int): Number of simulated draw counts
    entries(list of list): List containing bets
    """

    # Initialize list of number of draws
    nums = []

    while len(nums) != numSim:
        nums.append(ez_2(entries))

    # Create 'labels' list (list containing number of entries/bets)
    labels = [len(entries)] * numSim

    # Create results dataframe (Size: numSim x 2)
    data = {'Draws': nums, 'Entry': labels}
    df = pd.DataFrame(data)

    return df


def createDistHist(data):
    """
    Creates histogram of distribution of number of draws to win

    data(DataFrame): Long form results containing draw counts
    """

    sns.set_theme()

    # Creating histogram
    # sns.histplot(data=data, x="Draws", hue="Entry", element="step") # For single plot
    g = sns.FacetGrid(data, col="Entry")
    g.map(sns.histplot, "Draws")
    
    # Display the plot
    plt.show()


def ez_2(entries):
    """
    Returns number of draws to win 2D lotto

    entries (list of list): List of list of entry / bets
    """

    # Create numpy array of entries
    entries = np.array(entries, dtype=int)

    # Generate available numbers
    availableNumbers = np.array([x for x in range(1,32)], dtype=int)

    # Initialize random generator
    rng = np.random.default_rng()

    totalgames = 0

    numbers = np.zeros(2, dtype=int)

    # Run draws
    while np.all((entries == numbers), 1).any() == False: # For multiple entries

        # Generate numbers
        numbers = rng.choice(availableNumbers, size=2, replace=False)
        totalgames += 1
    
    return totalgames


def main():
    pass


if __name__ == "__main__":
    main()