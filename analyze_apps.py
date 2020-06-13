import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

full_data = pd.read_excel("/home/prajith_v/coding/to_be_analysed/stayfocused-21.xlsx")

for i in range(full_data.shape[0]):
    if full_data["Package"].values[i]=='SF---------------SF-----------------SF':
        cut = i-1
        break
analyze = full_data.loc[0:cut+1,'Package':'TF']
analyze["Name"].values[61] = "YouTube"
analyze["Name"].values[62] = "Sheets"

lis = []
for i in range(0,cut+1):
    tmp = [analyze["Package"].values[i],analyze["Name"].values[i]]
    lis.append(tmp)
    
l = []

data = full_data.loc[cut+7:,'Package':'TF']
for i in range(data.shape[0]):
    l.append(i)
data = data.set_index([l])
data = data.rename(columns={"Package": "Package", "Name": "End_time","TF":"Utilized_time"})

#this is the func which resolves how much time is assigned to each slot
def update(tmp,last_slot,end_time,utilized_time,start_day,last_date):
    
    #Finding the time slot where this process started
    start_slot =  math.floor(((end_time-utilized_time-(start_day+last_date*86400000))/(1000*60*60))/2)
    #print(start_slot)
    
    #if the process is opened in the same slot again
    if last_slot==start_slot:
        ad = ((tmp[last_slot]*1000)+utilized_time)/(2*60*60*1000)
        #if the total usage after opening the app is less than the remaining capacity of the slot
        if ad<1:
            tmp[last_slot] +=int(utilized_time/1000)
            return [tmp,0],[last_slot,0]
        #if the usage of the app extends to the next slot
        else:
            #assigning the present slot whith its max capacity and alculating the remaining usage of the app
            x = 2*60*60*1000-tmp[last_slot]*1000
            tmp[last_slot] = 2*60*60
            last_slot+=1
            #the remaining time divided by 2 hrs
            value = (utilized_time-x)/(2*60*60*1000)
            #now calculating the time which is assigned for each slot
            while(value>0):
                
                #if value is > 1 then the present slot is filled completely
                if value>1 and last_slot<12:
                    tmp[last_slot] = int(2*60*60)
                    last_slot+=1
                    value-=1
                
                #this means the present slot is not filled completely
                if value>0 and last_slot<12:
                    tmp[last_slot] = int(value*2*60*60)
                    value-=1
                    
                #if the app is used in the time slot of 12 AM and 1 AM
                if last_slot==12:
                    return [tmp,value*2*60*60*1000],[12,1]
                
            return [tmp,0],[last_slot,0]
        
    # if the process is not opened in the same slot then finalise the previous unfilled slots
    for i in range(last_slot,start_slot):
        last_slot+=1
    start_time = end_time-utilized_time
    
    #the remaining time divided by 2 hrs
    value = (utilized_time/(2*60*60*1000))
    
    #now allotting each slot with particular values
    while(value>0):
        #if value is > 1 then the present slot is filled completely
        if value>=1 and last_slot<12:
            tmp[last_slot]=2*60*60
            last_slot+=1
            value-=1
            continue
            
        #this means the present slot is not filled completely
        if value>0 and last_slot<12:        
            tmp[last_slot]=int(value*2*60*60)
            value-=1
            
        #if the app is used in the time slot of 12 AM and 1 AM    
        if last_slot==12:
            return [tmp,value*2*60*60*1000],[12,1]
        
        return [tmp,0],[last_slot,0]
        
#calculating the total time usage
def sums(ls):
    s =0
    for k in range(0,12):
        s = s + ls[k]
    return s
    
#this function is used for finalizing the previous days unfilled slots and assigning date and total time
def finalize(tmp,last_date,last_slot,):
    for i in range(last_slot,12):
        last_slot+=1
    tmp[12] = int(sums(tmp))
    tmp[13] = last_date
    last_date+=1
    return last_date,tmp
    
for i in range(len(lis)):
    print(str(i+1)+" "+str(lis[i][1]))
x = int(input("Enter the number to get the stats : "))
label = lis[(x)-1][0]
print(label)

time_slots = [2,4,6,8,10,12,14,16,18,20,22,24]
start_day = 1581618569091
last_date = 0
main_list=[]


tmp=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
last_slot=0
for i in range(data.shape[0]):
    #if data["End_Time"].value[i]-data["Utilized_time"].value[i]<(start_day+(last_date+1)*86400000):
    if data["Package"].values[i]==label:
        if (data["End_time"].values[i]-data["Utilized_time"].values[i])<(start_day+(last_date+1)*86400000):
            #update here
            x,y = update(tmp,last_slot,data["End_time"].values[i],data["Utilized_time"].values[i],start_day,last_date)
            tmp = x[0]
            value = x[1]
            last_slot = y[0]
            flag  = y[1]
            if flag==1:
                ##Code here for the action if there is a residue in the last process's utilized_time
                last_date,tmp = finalize(tmp,last_date,last_slot)
                main_list.append(tmp)
                tmp=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                last_slot = 0 
                x,y = update(tmp,last_slot,data["End_time"].values[i],value,start_day,last_date)
                tmp = x[0]
                last_slot = y[0]
                flag=0
                continue
            if flag==0:
                continue
        else:
            last_date,tmp = finalize(tmp,last_date,last_slot)
            main_list.append(tmp)
            tmp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            last_slot = 0
            x,y = update(tmp,last_slot,data["End_time"].values[i],data["Utilized_time"].values[i],start_day,last_date)
            tmp = x[0]
            value = x[1]
            last_slot = y[0]
            flag  = y[1]
            if flag==1:
                ##Code here for the action if there is a residue in the last process's utilized_time
                last_date,tmp = finalize(tmp,last_date,last_slot)
                main_list.append(tmp)
                tmp=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                last_slot = 0 
                x,y = update(tmp,last_slot,data["End_time"].values[i],value,start_day,last_date)
                tmp = x[0]
                last_slot = y[0]
                value = x[1]
                flag  =0
                continue
            if flag==0:
                continue
                
                
last_date,tmp = finalize(tmp,last_date,last_slot)
main_list.append(tmp)   
last_slot=0

for i in range(last_date,51):
    tmp=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    last_date,tmp = finalize(tmp,last_date,last_slot)
    main_list.append(tmp)
          
        
days = []
time = []
for i in range(0,len(main_list)):
    days.append((main_list[i][13]+1))
    time.append((main_list[i][12])/(60*60))

plt.plot(days,time)
plt.xlabel("days")
plt.ylabel("time in hrs")
plt.show()