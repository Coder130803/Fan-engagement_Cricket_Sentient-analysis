import pandas as pd
from collections import defaultdict
from extract_function import extract_function

#reading through the files 
file_events=open()
excel_dataEvents=file_events.readlines()
file_events.close()

file_HR=open()
excel_datauser=file_HR.readlines()
file_HR.close()





cells1=[]
cells2=[]





# Creating a dictionary for match events
match_data=dict()
ball_data = ""
inn_over_ball=""

## adding inningoverball or unique event entries to match_data using loop 
for entry in excel_dataEvents[1:]:
    data=entry.rstrip("\n")
    #cells1.append(data.split(","))
    cells1=data.split(",")
    over = cells1[4]
    #over_key = 'over_'+over
    ball=cells1[5]
    innings=cells1[3]
    if inn_over_ball != "":
        prev_inn_over_ball = inn_over_ball
        end_time =  match_data[prev_inn_over_ball]['start_time']
    else:
        end_time = "2023-05-06  13:32:36"
    inn_over_ball = innings+'.'+over+'.'+ball
    start_time = cells1[2]
    # print(start_time,end_time)
    six = cells1[7]
    four=cells1[6]
    wicket=cells1[9]
    runs=cells1[10]
    extra=cells1[8]
    
    match_data[inn_over_ball] = \
        {'over':int(over), \
         'ball':int(ball), \
         'inn': innings,\
         'start_time':start_time, \
         'end_time' : end_time, \
         'six':six ,\
         'four':four ,\
         'wicket':wicket ,\
         'runs':runs ,\
         'extra':extra, \
         'HR':"" , \
         'Sound':""}







user_data=defaultdict()
## creating one for loop just to initialize the dictionary for users
for entry in excel_datauser[1:]:
    data=entry.rstrip("\n")
    cells2=data.split(",")
    UserID=cells2[0]
    # user_data[timestamp]={"User":ID,"HR":HR,"Team_ID":Team_ID,"Device_ID":Device_ID }
    user_data[UserID]=defaultdict()
    user_data[UserID]['HR']=defaultdict()
    

##  one more for loop to add value for each user
for entry in excel_datauser[1:]:
    data=entry.rstrip("\n")
    cells2=data.split(",")
    UserHR=cells2[5]
    UserID=cells2[0]
    team_ID=cells2[1]
    timestamp=cells2[3]
    # print(timestamp)
    emotion=cells2[9]
    # time_user=timestamp+"_"+ID
    # Team_ID=cells2[1]
    # Team=cells2[3]
    # user_data[timestamp]={"User":ID,"HR":HR,"Team_ID":Team_ID,"Device_ID":Device_ID }
    user_data[UserID]['HR'][timestamp]=defaultdict()
    user_data[UserID]['HR'][timestamp]['current_HR']=UserHR
    user_data[UserID]['HR'][timestamp]['Expected_emotion']=emotion
    user_data[UserID]['HR'][timestamp]['Team_ID']=team_ID
   






#loop to add event in a time range according to timestamp of HR in dictionary 

num_users=len(user_data.keys())
print("INFO : Total NUmber of users : ", num_users)
for i in user_data.keys():
    for j in user_data[i]['HR'].keys():
        # print(i, j)
        user_data[i]['HR'][j]['six']="false"
        user_data[i]['HR'][j]['four']="false"
        user_data[i]['HR'][j]['wicket']="false"
        user_data[i]['HR'][j]['runs']="0"
        user_data[i]['HR'][j]['extra']="0"
        user_data[i]['HR'][j]['inn']="No event"
        user_data[i]['HR'][j]['over']="No event"
        user_data[i]['HR'][j]['ball']="No event/ball not in user data"
        user_data[i]['HR'][j]['ball_time']="HR timestamp not in ball range"
        
        for k in match_data.keys(): 
             
            if(extract_function.check_timestamp_between(j,match_data[k]['start_time'],match_data[k]['end_time'])):
                
                    #print(i+"--"+k+"--"+match_data[k]['start_time']+"< "+j+"< "+match_data[k]['end_time']+match_data[k]['six']+"HR : "+user_data[i]['HR'][j]['current_HR']) 
                    # print(i +"--"+k+"--"+"Six : "+match_data[k]['six']+" HR : "+user_data[i]['HR'][j]['current_HR']+"  Deviation : "+str(user_data[i]['HR'][j]['deviation_WHR']))

                    user_data[i]['HR'][j]['six']=match_data[k]['six']
                    user_data[i]['HR'][j]['four']=match_data[k]['four']
                    user_data[i]['HR'][j]['wicket']=match_data[k]['wicket']
                    user_data[i]['HR'][j]['runs']=match_data[k]['runs']
                    user_data[i]['HR'][j]['extra']=match_data[k]['extra']
                    user_data[i]['HR'][j]['inn']=match_data[k]['inn']
                    user_data[i]['HR'][j]['over']=match_data[k]['over']
                    user_data[i]['HR'][j]['ball']=match_data[k]['ball']
                    user_data[i]['HR'][j]['ball_time']=match_data[k]['start_time']
                #print("Debug : check 1")
        #print("Debug : check 2 : ",i,j)    
        # pd.set_option('display.max_columns', None)
    print("INFO : FInished Processing User  :",i)
    # df=pd.DataFrame(user_data[i])
    # #print(df)
    # df_2 = pd.DataFrame(df['HR'])
    # df_3 = pd.DataFrame(df_2)
    # #df_4 = pd.DataFrame(df_3[j])
    # print(df_2) 










## Eliminating anomoly of HR being excesssively high 
previous_timestamp=None
previous_user=None
for i in user_data.keys():
    for j in user_data[i]['HR'].keys():    
        
            if previous_user is None:
                    previous_user=i
                    previous_timestamp=j 

                    if int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])>=130:
                        user_data[previous_user]['HR'][previous_timestamp]['current_HR']="130"

            else:
                    current=i
                    if previous_user is current:
                        if int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])>=130:
                            user_data[previous_user]['HR'][previous_timestamp]['current_HR']="130"
                        
                    
                    previous_timestamp=j
                    previous_user=i       


## eliminating anomoly of unexpected HR trough   
previous_timestamp=None
previous_user=None
for i in user_data.keys():
    for j in user_data[i]['HR'].keys():    
        if previous_user is None:
                previous_user=i
                
                previous_timestamp=j  

                
                
                

                min_HRRange=round(int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])/1.5)
                min_hr=round(int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])/1.3)
                # print(min_HRRange)
                
                if int(user_data[previous_user]['HR'][j]['current_HR'])<min_HRRange:
                    user_data[previous_user]['HR'][j]['current_HR']=str(min_hr)     
                
        else:
                current=i
                if previous_user is current:
                    
                    

                    min_HRRange=round(int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])/1.5)
                    min_hr=round(int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])/1.3)
                    # print(max_HRRange)
                    
                    if int(user_data[previous_user]['HR'][j]['current_HR'])<min_HRRange:
                        user_data[previous_user]['HR'][j]['current_HR']=str(min_hr) 
                
                previous_timestamp=j
                previous_user=i




## eliminating anomoly of unexpected HR spike      
previous_timestamp=None
previous_user=None
for i in user_data.keys():
    for j in user_data[i]['HR'].keys():    
        if previous_user is None:
                previous_user=i
                
                previous_timestamp=j  

                
                
                max_HRRange=round(int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])*1.5)
                max_hr=round(int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])*1.3)

                
                # print(max_HRRange)
                int(user_data[previous_user]['HR'][j]['current_HR'])>max_HRRange
                if int(user_data[previous_user]['HR'][j]['current_HR'])>max_HRRange:
                    user_data[previous_user]['HR'][j]['current_HR']=str(max_hr)
                    
                
        else:
                current=i
                if previous_user is current:
                    
                    max_HRRange=round(int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])*1.5)
                    max_hr=round(int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])*1.3)

                    
                    # print(max_HRRange)
                    if int(user_data[previous_user]['HR'][j]['current_HR'])>max_HRRange:
                        user_data[previous_user]['HR'][j]['current_HR']=str(max_hr)
                     
                
                previous_timestamp=j
                previous_user=i
                
                
                


## Computing deviation of HR from previous entry for user
previous_timestamp=None
previous_user=None
# beforecurrent=None
# previous_timestamp2=None
for i in user_data.keys():
    for j in user_data[i]['HR'].keys():    
        if previous_user is None:
                previous_user=i
                # previous_timestamp2=previous_timestamp
                # if(previous_timestamp is j):
                #     print("yes")
                previous_timestamp=j
                
                deviation_prev=int(user_data[previous_user]['HR'][j]['current_HR'])-int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])
                # deviation_prev2="No data"
                # print(i,int(user_data[previous_user]['HR'][j]['current_HR']),j,int(user_data[previous_user]['HR'][previous_timestamp]['current_HR']),previous_timestamp, deviation_prev,)       
        else:
                current=i
                
                if previous_user is not current:
                    deviation_prev="Invalid : user change"
                #     deviation_prev2="Invalid: user change"

                # elif previous_user is not beforecurrent:
                #     deviation_prev2="Invalid: user change"    
                else:
                    deviation_prev=int(user_data[previous_user]['HR'][j]['current_HR'])-int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])
                    # deviation_prev2=int(user_data[previous_user]['HR'][j]['current_HR'])-(int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])+int(user_data[previous_user]['HR'][previous_timestamp])
                    
                
                    if previous_timestamp != None:
                        deviation_prev=int(user_data[previous_user]['HR'][j]['current_HR'])-int(user_data[previous_user]['HR'][previous_timestamp]['current_HR'])
                        
                    else:
                        deviation_prev=0
                
                # print(i,int(user_data[current]['HR'][j]['current_HR']),j,previous_timestamp)
                # beforecurrent=previous_user
                # previous_timestamp2=previous_timestamp    
                previous_timestamp=j
                previous_user=i
        user_data[i]['HR'][j]['deviation_FromPrev']=deviation_prev








# Output writing code block 
op_data=open('.csv', 'w')
Event_name=['Team_ID','ball_time','inn','over','ball','current_HR','deviation_FromPrev','six','four','wicket','runs','extra','Expected_emotion']
print("INFO : writing output file")
print("user,Timestamp",file=op_data,end="")
for k in Event_name:
    print(",",k,file=op_data,end="")
print("",file=op_data)
for i in user_data.keys():
    # print(i,file=op_data)
    for j in user_data[i]['HR'].keys():
        
        print(i,",",j,file=op_data,end="")
        
        for k in Event_name:
        # for k in user_data[i]['HR'][j].keys():
            # with open('C:\\Users\\sahil\\Data anlytics Internship_FanPlay\DATA\CSKvMI\\New Microsoft Excel Worksheet.csv','w') as output:
                print(",",str(user_data[i]['HR'][j][k]),file=op_data,end="")
        print("",file=op_data)

