import pandas as pd
import csv
import os
import matplotlib.pyplot as plt

temp_col=0
label_col=1

def find_vals(file, train=False): #returns a list of temperature profiles for each detected shower in df.
    df = pd.read_excel(file, sheet_name="DATA", usecols='C,D', skiprows = 1)
    data = df.iloc[:,temp_col].to_list()
    n = 0
    vals = []
    det_starts = []
    gt_starts = []
    gt_ends = []
    start_index = -1
    print("detected:")
    while n <= len(data)-3:
        if all(data[i+1]-data[i]>=0.1 for i in range(n,n+3)):
            if start_index == -1:
                start_index = n
        if start_index != -1 and all(data[i+1]<data[i] for i in range(n,n+3)):
            end_index = n
            det_starts.append(start_index)
            vals.append([t for t in data[start_index:end_index]])
            start_index = -1
        n+=1
    if train:
        print("groundtruth:")
        durs=[]
        labels = df.iloc[:,label_col].to_list()
        n = 0
        while n<len(labels):
            if str(labels[n]).startswith('Start'):
                gt_starts.append(n)
                start = n
            if str(labels[n]).startswith('End'):
                end = n
                gt_ends.append(n)
                durs.append(end-start)
            n+=1
        print(f"gt: {len(durs)}, detected: {len(vals)}")
        print(gt_starts)
        plt.plot(range(len(data)),data)
        plt.ylabel(u"T (\N{DEGREE SIGN}F)")
        plt.xlabel("index")
        plt.title(f"Groundtruthed Temperature Data: {file[8:16]}")
        plt.scatter(gt_starts,[data[i] for i in gt_starts], label="Starts")
        #plt.scatter(gt_ends,[data[i] for i in gt_ends], label="Ends")
        plt.scatter(det_starts,[data[i] for i in det_starts], label="Detected Starts")
        plt.legend()
        plt.show()
    return
            
def main():
    os.chdir('data')
    find_vals(os.listdir()[2], True)
    
main()
