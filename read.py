import pandas as pd
from matplotlib import pyplot as plt
import sqlite3
 

def main():

    DATA_URL = 'drawresults.htm'

    df = getData(DATA_URL)

    createDB(df)


def createDB(df):
    """
    Creates SQL database of results

    df: DataFrame of results
    """

    conn = sqlite3.connect('results.sqlite')
    cur = conn.cursor()

    # Set-up tables
    cur.executescript('''
    DROP TABLE IF EXISTS LottoType;   
    DROP TABLE IF EXISTS DrawInfo; 
    DROP TABLE IF EXISTS Combinations; 

    CREATE TABLE LottoType (
        id          INTEGER PRIMARY KEY,
        lottotype   TEXT UNIQUE
    );                   

    CREATE TABLE DrawInfo (
        id              INTEGER PRIMARY KEY,
        ballcount       INTEGER,
        type_id         INTEGER,    
        draw_date       TEXT,
        jackpot         REAL,
        winnercount     INTEGER,
        FOREIGN KEY(type_id) REFERENCES LottoType(id)   
    );       

    CREATE TABLE Combinations (
        results_id  INTEGER,
        n1          INTEGER,
        n2          INTEGER,     
        n3          INTEGER,     
        n4          INTEGER,            
        n5          INTEGER,
        n6          INTEGER,    
        FOREIGN KEY(results_id) REFERENCES DrawInfo(id)        
    )
    ''')

    # Inserting data into database
    for index, row in df.iterrows():
        
        ballcount = len(row['COMBINATIONS'])
        draw_date = row['DRAW DATE'].strftime("%Y-%m-%d")
        jackpot = row['JACKPOT (PHP)']
        winnercount = row['WINNERS']

        # Inserting lottery type
        cur.execute('''INSERT OR IGNORE INTO LottoType (lottotype)
            VALUES ( ? )''', ( row['LOTTO GAME'], ) )
        cur.execute('SELECT id FROM LottoType WHERE lottotype = ? ', (row['LOTTO GAME'], ))
        type_id = cur.fetchone()[0]

        # Inserting DrawInfo table entry - type_id, draw date, jackpot, winnercount
        cur.execute('''INSERT OR REPLACE INTO DrawInfo
            (ballcount, draw_date, jackpot, winnercount, type_id) VALUES ( ?, ?, ?, ?, ? )''',
            (ballcount, draw_date, jackpot, winnercount, type_id) )
        cur.execute('SELECT id FROM DrawInfo WHERE type_id = ? AND draw_date = ? ', (type_id, draw_date))
        results_id = cur.fetchone()[0]

        # Reassignment for shorter name (for next step / inserting combinations)
        n = row['COMBINATIONS']

        # Inserting combinations
        if ballcount == 6:
            cur.execute('''INSERT OR REPLACE INTO Combinations
                (results_id, n1, n2, n3, n4, n5, n6) VALUES ( ?, ?, ?, ?, ?, ?, ?)''',
                (results_id, n[0], n[1], n[2], n[3], n[4], n[5]) )
        elif ballcount == 5:
            cur.execute('''INSERT OR REPLACE INTO Combinations
                (results_id, n1, n2, n3, n4, n5) VALUES ( ?, ?, ?, ?, ?, ?)''',
                (results_id, n[0], n[1], n[2], n[3], n[4]) )
        elif ballcount == 4:
            cur.execute('''INSERT OR REPLACE INTO Combinations
                (results_id, n1, n2, n3, n4) VALUES ( ?, ?, ?, ?, ?)''',
                (results_id, n[0], n[1], n[2], n[3]) )
        elif ballcount == 3:
            cur.execute('''INSERT OR REPLACE INTO Combinations
                (results_id, n1, n2, n3) VALUES ( ?, ?, ?, ?)''',
                (results_id, n[0], n[1], n[2]) )
        elif ballcount == 2:
            cur.execute('''INSERT OR REPLACE INTO Combinations
                (results_id, n1, n2) VALUES ( ?, ?, ?)''',
                (results_id, n[0], n[1]) )
        else:
            raise Exception("Ball count not within range 2-6")
        
    conn.commit()
    cur.close()


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