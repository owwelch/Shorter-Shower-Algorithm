import pandas as pd
import time
import csv
import os

def find_vals(df):
    data = df.iloc[:,0].to_list()
    n = 0
    vals = []
    while n < len(data)-8:
        t = True
        for i in range(n, n+3):
            if data[i+1] - data[i] < 0.1:
                t = False
                n = i+1
                break
        if t:
            start_index = n
            n += 3
            peak_index = -1
            while peak_index == -1:
                t = True
                for j in range(n, n+3):
                    if data[j] < data[j+1]:
                        t = False
                        n = j+1
                        break
                if t:
                    end_index = n
                    vals.append([t for t in data[start_index:end_index])
    return(vals)
            
def main():
    os.chdir('data')
    file = os.listdir()[0]
    df = pd.read_excel(file, sheet_name="DATA", usecols='B')
    vals = find_vals(df)
    result = open(os.path.abspath(os.getcwd())+ "\\results.csv", "x")
    csvwriter = csv.writer(result, lineterminator = '\n')
    header = ["start time","start temp (F)","stop time","stop temp (F)","peak time","peak temp(F)","duration (s)", '', "start row", "stop row", "peak row"]
    csvwriter.writerow(header)
    for i in range(len(vals)):
        csvwriter.writerow(vals[i])
    print("Done!")
    result.close()

main()
