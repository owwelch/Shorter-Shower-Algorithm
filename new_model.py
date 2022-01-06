import pandas as pd
import os
import matplotlib.pyplot as plt

#temp readings are 20s apart

temp_col=0
label_col=1

def find_vals(file, vals): #returns a list of temperature profiles for each detected shower in df.
    df = pd.read_excel(file, sheet_name="DATA", usecols='C,D', skiprows = 1)
    data = df.iloc[:,temp_col].to_list()
    n = 0
    vals = []
    target = []
    start_index = -1
    print(data[1305])
    while 1:
        if all(data[i+1]-data[i]>=0.1 for i in range(n,n+3)):
            if start_index == -1:
                start_index = n
        if start_index != -1 and all(data[i+1]<data[i] for i in range(n,n+3)):
            end_index = n
            vals.append([t for t in data[start_index:end_index]])
            while n<len(data) and pd.isna(data[n]):
                n+=1
            if n>=len(data):
               break
            start_index = -1
        n+=1
        labels = df.iloc[:,label_col].to_list()
    n = 0
    while n<len(labels):
        if str(labels[n]).startswith('Start'):
            print(labels[n])
            start = n
        if str(labels[n]).startswith('End'):
            end = n
            target.append(end-start)
        n+=1
    return
            
def main():
    os.chdir('data')
    print(find_vals('Reduced Kahn S2c 20569773 2019-04-26 09_54_34 -0400.xlsx', []))
    
main()
