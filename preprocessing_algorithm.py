import numpy as np
from collections import defaultdict
import statistics
from extract_function import extract_function



## accessing data from datafile
file_trainingdata=open()# input your collected heart rate data and events file from match 
excel_trainingdata=file_trainingdata.readlines()
file_trainingdata.close()

cells1=[]

## creating userdatabase using dictionary 
user_data=defaultdict()
for entry in excel_trainingdata[1:]:
    
    data=entry.rstrip("\n")
    cells1=data.split(",")
    
    UserID=cells1[9]
    user_data[UserID]=defaultdict()# using defaultdict for nested dictionary structure for better access 
    
    

for entry in excel_trainingdata[1:]:
    data=entry.rstrip("\n")
    cells1=data.split(",")
    
    UserID=cells1[9]
    timestamp=cells1[6]
    team=cells1[4]
    batting_ID=cells1[2]
    bowling_ID=cells1[3]
    innings=cells1[7]
    HR=cells1[10]
    Sound=cells1[8]
    deviation=cells1[11]
    Variance=cells1[12]
    wtVariance=cells1[16]
    over=cells1[17]
    dvar=cells1[13]
    CI=cells1[14]
    Hr_Zone=cells1[15]
    event=cells1[18]
    


    user_data[UserID][timestamp]=defaultdict()
    
    user_data[UserID][timestamp]['event']=int(event)
    user_data[UserID][timestamp]['HR']=float(HR)
    user_data[UserID][timestamp]['over']=float(over)
    user_data[UserID][timestamp]['inning']=innings
    user_data[UserID][timestamp]['batting_ID']=int(batting_ID)
    user_data[UserID][timestamp]['bowling_ID']=int(bowling_ID)
    user_data[UserID][timestamp]['team']=int(team)





    
    

                       

## create Variance values 
j_=None
j__ = None
i__=None
i_=None
for i in user_data.keys():
    for j in user_data[i].keys():
        user_data[i][j]["Variance"]=0
        if i__==i and i_==i:
            HR_values=[user_data[i][j__]['HR'],user_data[i][j_]['HR'],user_data[i][j]['HR']]
            user_data[i][j]["Variance"]=statistics.variance(HR_values)

        #print(user_data[i][j]["Variance"])
        j__ = j_
        j_=j
        i__=i_
        i_=i    


## map variance values with events and matchstate using pre-determined metrics 
for i in user_data.keys():
    for j in user_data[i].keys():
        user_data[i][j]['matchstate']=1
       
        if user_data[i][j]['inning']=="I":
            
            
            if user_data[i][j]['over']<=6:
                if user_data[i][j]['event']==4:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=1.25
                    else:
                        user_data[i][j]['matchstate']=-1.25
                
                elif user_data[i][j]['event']==6:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=1.75
                    else:
                        user_data[i][j]['matchstate']=-1.75                    
                
                elif user_data[i][j]['event']==23:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=1.125
                    else:
                        user_data[i][j]['matchstate']=-1.125    
                
                elif user_data[i][j]['event']==0:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=-1.5
                    else:
                        user_data[i][j]['matchstate']=1.5    
            
            
            
            elif user_data[i][j]['over']<=15:
                if user_data[i][j]['event']==4:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=1.875
                    else:
                        user_data[i][j]['matchstate']=-1.875
                
                elif user_data[i][j]['event']==6:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=2.625
                    else:
                        user_data[i][j]['matchstate']=-2.625                    
                
                elif user_data[i][j]['event']==23:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=1.688
                    else:
                        user_data[i][j]['matchstate']=-1.688   
                
                elif user_data[i][j]['event']==0:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=-2.25
                    else:
                        user_data[i][j]['matchstate']=2.25
            
            
            
            elif user_data[i][j]['over']<=20:
                if user_data[i][j]['event']==4:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=2.5
                    else:
                        user_data[i][j]['matchstate']=-2.5
                
                elif user_data[i][j]['event']==6:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=3.5
                    else:
                        user_data[i][j]['matchstate']=-3.5                    
                
                elif user_data[i][j]['event']==23:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=2.25
                    else:
                        user_data[i][j]['matchstate']=-2.25   
                
                elif user_data[i][j]['event']==0:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=-3
                    else:
                        user_data[i][j]['matchstate']=3
        
        
        
        
        
        else:
            if user_data[i][j]['over']<=6:
                if user_data[i][j]['event']==4:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=2.5
                    else:
                        user_data[i][j]['matchstate']=-2.5
                
                elif user_data[i][j]['event']==6:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=3.5
                    else:
                        user_data[i][j]['matchstate']=-3.5                    
                
                elif user_data[i][j]['event']==23:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=2.25
                    else:
                        user_data[i][j]['matchstate']=-2.25   
                
                elif user_data[i][j]['event']==0:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=-3
                    else:
                        user_data[i][j]['matchstate']=3   
            
            
            
            elif user_data[i][j]['over']<=15:
                if user_data[i][j]['event']==4:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=3.75
                    else:
                        user_data[i][j]['matchstate']=-3.75
                
                elif user_data[i][j]['event']==6:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=5.25
                    else:
                        user_data[i][j]['matchstate']=-5.25                    
                
                elif user_data[i][j]['event']==23:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=3.375
                    else:
                        user_data[i][j]['matchstate']=-3.375   
                
                elif user_data[i][j]['event']==0:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=-4.5
                    else:
                        user_data[i][j]['matchstate']=4.5
            
            
            
            elif user_data[i][j]['over']<=20:
                if user_data[i][j]['event']==4:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=5
                    else:
                        user_data[i][j]['matchstate']=-5
                
                elif user_data[i][j]['event']==6:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=7
                    else:
                        user_data[i][j]['matchstate']=-7                    
                
                elif user_data[i][j]['event']==23:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=4.5
                    else:
                        user_data[i][j]['matchstate']=-4.5   
                
                elif user_data[i][j]['event']==0:
                    if user_data[i][j]['batting_ID']==user_data[i][j]['team']:
                        user_data[i][j]['matchstate']=-6
                    else:
                        user_data[i][j]['matchstate']=6
count=0
totalcount=0






## adding compounding effect to CI to reflect previous ball impact
j_=None
j__=None
i_=None
i__=None
for i in user_data.keys():
    for j in user_data[i].keys():
        
        if i__==i and i_==i:
            if j__!=None and j_!= None:
                if user_data[i][j_]['matchstate'] != 1 and user_data[i][j__]['matchstate'] != 1 :
                    if extract_function.is_time_difference_within_2_minutes(j__,j_):
                        user_data[i][j_]['matchstate']=user_data[i][j_]['matchstate']+round(0.25*user_data[i][j__]['matchstate'],3)
        j__ = j_
        j_=j
        i__=i_
        i_=i  




j_=None ## previous ball
j__=None ## 2 balls before
i_=None ## previous user entry
i__=None ## 2 users before entry 

for i in user_data.keys():
    for j in user_data[i].keys():
        
        if i__==i and i_==i:
            if j__!=None and j_!= None:
                if user_data[i][j_]['matchstate'] == 1:
                        if user_data[i][j__]['matchstate']>=5:
                            user_data[i][j_]['matchstate']= user_data[i][j__]['matchstate'] - 2 
                            #user_data[i][j]['matchstate']=1
                        elif user_data[i][j__]['matchstate']<=-5:
                            user_data[i][j_]['matchstate']= user_data[i][j__]['matchstate'] + 2 
                            #user_data[i][j]['matchstate']=1
                        elif user_data[i][j__]['matchstate']<5 and user_data[i][j__]['matchstate'] >=2 :
                            user_data[i][j_]['matchstate']= user_data[i][j__]['matchstate'] - 1 
                            #user_data[i][j]['matchstate']=1
                        elif user_data[i][j__]['matchstate']>-5 and user_data[i][j__]['matchstate'] <=-2 :
                            user_data[i][j_]['matchstate']= user_data[i][j__]['matchstate'] + 1 
                            #user_data[i][j]['matchstate']=1
        j__ = j_
        j_=j
        i__=i_
        i_=i  

                

## calculating weighted Variance for emotion mapping
for i in user_data.keys():
    for j in user_data[i].keys():
        user_data[i][j]['wtVariance']=round(user_data[i][j]['Variance']*user_data[i][j]['matchstate'],3)

## mapping wtVariance with emotion labels 
for i in user_data.keys():
    for j in user_data[i].keys():
        user_data[i][j]['Emotion']=extract_function.classify_emotion(user_data[i][j]['wtVariance'])
        #print(user_data[i][j]['wtVariance'],user_data[i][j]['Emotion'])
        

## inputting data into a csv 
op_data=open('training_file.csv','w')
event_name=['team','over','event','HR','Variance','matchstate','wtVariance','Emotion']
print("INFO : writing input file")
print('User,Timestamp',file=op_data,end="")
for k in event_name:
    print(",",k,file=op_data,end="")
print("",file=op_data)
for i in user_data.keys():
    for j in user_data[i].keys():
        print(i,",",j,file=op_data,end="")
        for k in event_name:
           print(",",str(user_data[i][j][k]),file=op_data,end="")
        print("",file=op_data)