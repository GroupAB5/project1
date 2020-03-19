import numpy as np
from os import listdir
from os.path import isfile, join
import Quality_Assessment as qa

# covariance data from module Quality_Assessment
def get_sorted_matrix():
    # returns a list of sublists per station with all covariance matrices for that station
    cov_data = []
    mypath = r'C:\Users\Mees de Graaf\Documents\Tu delft\project test analysis\GPS_Data\data'
    filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))] # getting all filenames in a list
    for file in filenames:
        if len(file) == 15: # only files with the regular filename should pass
            cov_data.extend(qa.get_covmatrix(file))

    # lambda function used to sort the list of covariances with
    cov_data.sort(key = lambda x:x[0][0:6])

    # Getting a list of station names
    with open(join(r'C:\Users\Mees de Graaf\Documents\Tu delft\project test analysis\GPS_Data', 'sitelist.txt')) as f:
        stations = f.readlines()
    poss_tags = [station[0:4] for station in stations] # all station names from "sitelist.txt"

        # counting occurences of stations
    tags = [entry[0][0:4] for entry in cov_data] # all tags from all files
    tagcounts = [tags.count(ptag) for ptag in poss_tags] # number of occurences of a certain tag (number of matrices per station)
    varnumber = [sum(tagcounts[0:i]) for i in range(len(tagcounts)+1)] # trick to splice the list
    cov_final = [cov_data[varnumber[i]:varnumber[i+1]] for i in range(len(tagcounts))] # list is spliced per station
    return cov_final # the order of sorting is almost correct except that 1999 is at the end instead of beginning

if __name__ == '__main__':
    print(get_sorted_matrix()[0]) # prints all matrices for station "ALGO"
