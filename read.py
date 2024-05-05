import pandas as pd
from matplotlib import pyplot as plt
 

def main():

    DATA_URL = 'drawresults.htm'

    df = getData(DATA_URL)


def createHist(data, numCount, typeTitle):
    """
    Plots histogram

    data(list): pooled dataset of draws
    numCount(int): number of unique numbers in lottery type (e.g. 55 for 6/55 Grand Lotto)
    typeTitle(str): lotto type, used for title
    """
    plt.hist(data, bins=numCount, alpha=0.5)
    plt.title(f'Number Distribution for {typeTitle}')
    plt.xlabel('numbers')
    plt.ylabel('count')
    plt.show()


def createUniformData(data, numCount):
    """
    Returns a data of uniformly distributed draws
    
    data(list): pooled dataset of draws
    numCount(int): number of unique numbers in lottery type (e.g. 55 for 6/55 Grand Lotto)
    """
    valCount = round(len(data) / numCount) # Number of draws per number in a uniform

    uniformData = []

    for num in range(min(data), numCount + 1):
        for _ in range(valCount):
            uniformData.append(num)

    return uniformData


def poolCombination(s):
    """
    Returns a pooled / flattened list from all combination lists

    s: data series of combinations
    """

    # Convert series to list
    listOfList = s.to_list()

    # Obtained pooled / flattened list
    flatList = [
        val
        for combiList in listOfList
        for val in combiList
    ]

    return flatList


def combiToInt(x):
    """
    Convert list of strings to list of int (used for combinations column)

    x (list): List of combination
    """

    try: 
        return [int(i) if i == '0' else int(i.lstrip("0")) for i in x]
    except:
        raise Exception(f"Unable to convert to int due to {x}, remove this data")


def getData(DATA_URL):
    """
    Returns a dataframe of results

    DATA_URL (str): page containing table
    """

    # Parse HTML tables from page (set first row as header)
    html_tables = pd.read_html(DATA_URL, header=0)

    # Get dataframe of results
    df = html_tables[0]

    # Process and clean data
    df['DRAW DATE']= pd.to_datetime(df['DRAW DATE']) # object -> datetime
    df['COMBINATIONS'] = df['COMBINATIONS'].str.split('-') # Reformat to list 
    invalidVals = [['', ''], ['', '', '']] # Invalid combination values
    df = df[~df['COMBINATIONS'].isin(invalidVals)] # Removing rows with invalid combination values
    df.loc[:,'COMBINATIONS'] = df['COMBINATIONS'].apply(lambda x: combiToInt(x)) # Convert combination string list to integer list

    # Filter out data which type has fewer than 100 occurence (arbitrarily selected) - filtered due to "insufficient" data 
    minLottoTypeOccurence = 100
    counts = df['LOTTO GAME'].value_counts(ascending=False)
    countsToRemove = counts[counts < minLottoTypeOccurence]
    typeToRemove = countsToRemove.index.values.tolist()
    df = df[~df['LOTTO GAME'].isin(typeToRemove)]

    return df


if __name__ == "__main__":
    main()