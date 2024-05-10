import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def gen_ez_2dist(numSim, entries):
    """
    Generates list of number of draws
    """

    # Initialize list of number of draws
    nums = []

    while len(nums) != numSim:
        nums.append(ez_2(entries))

    return nums


def createDistHist(data):
    """
    Creates histogram of distribution of number of draws to win
    """
    # Creating histogram with density plot
    sns.histplot(data, bins=50, kde=True, color='lightgreen', edgecolor='red')
    
    # Adding labels and title
    plt.xlabel('Values')
    plt.ylabel('Draws')
    plt.title(f'Number of draws to win (N = {len(data)})')
    
    # Display the plot
    plt.show()

    return np.mean(data)


def ez_2(entries):
    """
    Returns number of draws to win 2D lotto
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
    while np.array_equal(entries, numbers) == False: 

        # Generate numbers
        numbers = rng.choice(availableNumbers, size=2, replace=False)
        totalgames += 1
    
    return totalgames


def main():
    pass


if __name__ == "__main__":
    main()