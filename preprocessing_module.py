import pandas as pd
import numpy as np
from sklearn import preprocessing



def object_checking(df):
    """ A function that checks for String objects in data """
    object_value = df.select_dtypes(include='object')
    arr = np.array(object_value)

    if arr.dtype == 'object':
        print('Error: string-object in column: ' + str(object_value.columns[0])+'. Correct your data to a numeric type.')
    else:
        print('Correct data.')

# def comas_to_dots(df):
#     """ Convert dots to commas in floating-point numbers """
#     df = pd.read_csv("C:/Users/danie/Desktop/ClusterProject/gini.csv", sep=";")
#     df.to_csv("gini_dot.csv", sep='\t', encoding='utf-8', decimal='.')


def header_checking(df):
    """ Check if all columns have headers """

    headers = df.columns.str.contains('^Unnamed')

    if True in headers:
        print('Warning! Missing values in data. Please, complete headers in your data.')
    else:
        print('Your dataset is correct.')


def data_completeness(df):
    """ Function to check if all data has been completed. It checks whether there are nissing values """

    for key, value in df.iteritems():

        nan_value = value.hasnans
        if nan_value is True:
            print('Warning!', value.hasnans.sum(), 'uncompleted data at:\n', df[df.isnull().T.any().T])
        elif 'object' in df.dtypes:
            print('Warning! String object.')
        else:
            """" Export data after standardization to internal file (memory) """
            df.to_csv('C:/Users/danie/Desktop/ClusterProject/giniInner.csv', sep="\t", header=True)


def variable_renaming(df):
    """ A function that checks whether each variable has its own name. If so-assigns names to index rows and deletes the first column with names. If not, number them starting with 1.. """
    print('Do the data in each row of the data set have variable names? [y/n] ')
    var_names = str(input())
    df.index.names = ['Name']
    if var_names.lower() == 'y':
        df = df.rename(df.iloc[:, 0])
        df = df.drop(list(df)[0], axis=1)
        return df
    else:
        n = df.shape[0]
        df.index = range(1, n+1)
        return df


def standarize(df):
    x = df.iloc[:, 1:].values
    standscaler = preprocessing.StandardScaler()
    standscaler_df = standscaler.fit_transform(x)
    st_df = pd.DataFrame(standscaler_df)
    print("Standarized data: \n", st_df)
    print("Average: ", st_df.mean(axis=0))
    print("Standard deviation: \n", st_df.std(axis=0))

