import xlsxwriter

def ex_output(fileName, calcStart, calcPeak, giveStart, givePeak):
    workbook = xlsxwriter.Workbook('Output ' + fileName)
    # Here is what we do here: We want to print every row with a list of what it is: (Start, Peak, Given Start, etc)
    # Followed by time and temperature.
