import csv  

variables = ['type', 'grid', 'count', 'time']
#type: h - high resolutin, l  - low resolution, 1 - scenario 1 (fixed path), 2 - scenario 2(follow currents)
#example h_1 = high resolution grid with fixed path
filename = "over_time.csv"

# writing to csv file  
with open(filename, 'a') as csvfile:  
    csvwriter = csv.writer(csvfile)   
    csvwriter.writerow(variables)  
