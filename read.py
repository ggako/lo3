import pandas as pd
 

def main():

    DATA_URL = 'drawresults.htm'

    df = getData(DATA_URL)


def combiToInt(x):
    """
    Convert list of strings to list of int (used for combinations column)
    """

    try: 
        return [int(i) if i == '0' else int(i.lstrip("0")) for i in x]
    except:
        print(x)
        # pass
        raise Exception(f"Unable to convert to int due to {x}, remove this data")


def getData(DATA_URL):
    """
    Returns a dataframe of results
    """

    # Parse HTML tables (set first row as header)
    html_tables = pd.read_html(DATA_URL, header=0)

    # Get dataframe of results
    df = html_tables[0]

    # Process and clean data
    df['DRAW DATE']= pd.to_datetime(df['DRAW DATE']) # object -> datetime
    df['COMBINATIONS'] = df['COMBINATIONS'].str.split('-') # Reformat to list 
    invalidVals = [['', ''], ['', '', '']] # Invalid combination values
    df = df[~df['COMBINATIONS'].isin(invalidVals)] # Removing rows with invalid combination values
    df.loc[:,'COMBINATIONS'] = df['COMBINATIONS'].apply(lambda x: combiToInt(x)) # Convert combination string list to integer list

    return df


if __name__ == "__main__":
    main()