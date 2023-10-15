import numpy as np
import tensorflow as tf
import statistics
from collections import defaultdict
from tensorflow import _keras
from keras.layers import Embedding, LSTM, Dense,Dropout,Bidirectional
from keras.callbacks import ModelCheckpoint,EarlyStopping
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import LabelEncoder
from matplotlib import pyplot
from extract_function import extract_function






## accessing data from datafile
file_trainingdata=open()# input your .csv file here 
excel_trainingdata=file_trainingdata.readlines()
file_trainingdata.close()

cells1=[]# list to store row entries from spreadsheet 

## creating user database using dictionary 
user_data=defaultdict()
for entry in excel_trainingdata[1:]:
    
    # splitting row entries to extract relevant features
    data=entry.rstrip("\n")
    cells1=data.split(",") 
    userID=cells1[0]
    user_data[userID]=defaultdict()

for entry in excel_trainingdata[1:]:
    data=entry.rstrip("\n")
    cells1=data.split(",")
    timestamp=cells1[1]
    event= cells1[4]
    HR=cells1[5]
    variance=cells1[6]
    wtvariance=cells1[8]
    emotion=cells1[9]

    user_data[userID][timestamp]=defaultdict()# use default dict to create nested dictionary system for easy acess 
    user_data[userID][timestamp]['event']=int(event)
    user_data[userID][timestamp]['HR']=float(HR)
    user_data[userID][timestamp]['variance']=float(variance)
    user_data[userID][timestamp]['wtvariance']=float(wtvariance)
    
    user_data[userID][timestamp]['emotion']=emotion


## Append data from dictionary into sequences and labels for later use in training 
sequences = []
labels = []
previous_timestamp=None
pre2timestamp = None
pre2user=None
previous_user=None

for i in user_data.keys():
   
    firstdata=True
    seconddata=True
    for j in user_data[i].keys():
        
        pre2sequence=[]
        presequence=[]
        sequence=[]
        aftersequence=[]
        ## loop through to go over all indicators of one user for one timestamp
        for k in user_data[i][j].keys():
            
            if k != 'emotion':
                
                
                
                ## first user entry or user change
                    if previous_user ==None or previous_user!=i:
                        sequence.append(user_data[i][j][k])
                    
                    else:
                        if previous_user==i:
                            presequence.append(user_data[i][previous_timestamp][k])
                            sequence.append(user_data[i][j][k])
                            
                            if pre2timestamp is not None:
                                if pre2user == i:
                                    pre2sequence.append(user_data[i][pre2timestamp][k])
            else:
            
                    
                    labels.append(user_data[i][j][k].strip())
                   
                  
        
      # Storing sequences in to show last two balls in cricket match 
        if firstdata:
            t_seq=np.array([sequence,sequence,sequence],dtype=np.float32)
            firstdata=False
           
        
        elif seconddata:
            t_seq=np.array([presequence,presequence,sequence],dtype=np.float32)
            seconddata=False
        elif firstdata!=True and seconddata!=True:
            t_seq=np.array([pre2sequence,presequence,sequence],dtype=np.float32)
          
        sequences.append(t_seq)     
        pre2timestamp = previous_timestamp
        previous_timestamp=j
        pre2user=previous_user
        previous_user=i                         




## normalising the data to between -1 to 1 for tanh activation function
data_min = np.min(sequences)
data_max = np.max(sequences)

sequences=2 * (sequences - data_min) / (data_max - data_min) - 1


# # print(set(labels))
# 1Amused
# 2Angry
# 3Calm
# 4Content
# 5Delighted
# 6Depressed
# 7Despair
# 8Disheartned
# 9Dismay
# 10Ecstatic
# 11Elated
# 12Excited
# 13Frustrated
# 14Happy
# 15Irritated
# 16Stressed
# 17Upset
# t_labels=[s.replace("Amused","1") for s in labels]
# print(t_labels)


# encoding labels 

label_array=[set(labels)]
#print(label_array)
encoded_labels=labels
count=0
for i in sorted(label_array[0]):
    encoded_labels=[s.replace(i,str(count)) for s in encoded_labels]
    count+=1
    
    





# Split data into training and testing sets
split = int(0.8 * len(sequences))
train_sequences = sequences[:split]
train_labels = encoded_labels[:split]
test_sequences = sequences[split:]
test_labels = encoded_labels[split:]



train_sequences=np.array(train_sequences)

test_sequences=np.array(test_sequences)


# generate categorical variables for model 
train_labels=_keras.utils.to_categorical(train_labels)
test_labels=_keras.utils.to_categorical(test_labels)


# Build the RNN model using LSTM
#initializer = tf.keras.initializers.GlorotUniform(seed=42)
model = tf.keras.Sequential()

model.add(Bidirectional(LSTM(128,return_sequences=True,input_shape=(3,4)))) ## input LSTM layer

model.add(Dropout(0.5))


model.add(Bidirectional(LSTM(128,activation='tanh',return_sequences=True)))

model.add(Dropout(0.5))

model.add(Bidirectional(LSTM(128,activation='tanh',return_sequences=True)))

model.add(Dropout(0.5))

model.add(Bidirectional(LSTM(128,activation='tanh',return_sequences=True)))

model.add(Dropout(0.5))

model.add(Bidirectional(LSTM(128,activation='tanh',return_sequences=False))) ## Final LSTM layer

model.add(Dropout(0.5))


model.add(Dense(17 , activation='softmax')) ## Output layer

model_callbacks = [EarlyStopping(monitor='val_loss', patience=3),\
            ModelCheckpoint(
                filepath='training_model_event_HR_var_over_tanh_addweights_29.h5',  # Path to save the best model
                monitor='val_loss',  # Metric to monitor
                save_best_only=True,  # Save only the best model
                save_weights_only=False,  # Save only the model weights
                verbose=1
            )]
# for i in model.inputs:
    
#     print(i.shape,"---" ,train_sequences.shape)
# for o in model.outputs:
#     print(o.shape,"----",train_labels.shape) 

# Compile the model
model.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])


history=model.fit(train_sequences, train_labels, epochs=20, batch_size=256,callbacks=model_callbacks,validation_data=(test_sequences,test_labels))
print(model.summary())
print(model.evaluate(test_sequences,test_labels,verbose=0))

# plot train and validation loss
pyplot.plot(history.history['loss'])
pyplot.plot(history.history['val_loss'])
pyplot.title('model train vs validation loss')
pyplot.ylabel('loss')
pyplot.xlabel('epoch')
pyplot.legend(['train', 'validation'], loc='upper right')
pyplot.show()


