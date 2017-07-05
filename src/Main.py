import os
import json
from collections import OrderedDict
from Function_Definitions import *

parent_path = os.getcwd()

friends = {} # friends network represented by dictionary of lists
anomalies = [] # anomalies represented by list of dictionaries
records=[] # purchase records represented by list of dictionaries

# Open batch_log.json
# Save purchase events in "records"
# Update "friends" for each befriend/unfriend event
filename = os.path.join(parent_path, 'log_input' ,'batch_log.json')
with open(filename, 'r') as f:
    check =-1
    for line in f:
        if line.strip(): # to avoid empty lines
            update = json.loads(line,object_pairs_hook=OrderedDict)
            if check ==-1:
                D = int(update['D']) # number of degrees
		if D<1:
		    print ('D should be an integer greater than 0. D='+str(update['D'])+' found.\nUsing D=1 instead')
		    D = 1
                T = int(update['T']) # tracked number of purchases
		if T<2:
		    print ('T should be an integer greater than 1. T='+str(update['T'])+' found.\nUsing T=2 instead')
		    T = 2
                check += 1
            elif update['event_type'] == 'purchase':
                del update['event_type']
                update['amount'] = float(update['amount'])
                records.append(update) 
            elif update['event_type'] == 'befriend' or update['event_type'] == 'unfriend':
                UpdateFriends(friends,update)
	    else:
		print('Unrecognized event type \"'+update['event_type']+'\". Skipping line')

# Open stream_log.json
# Save purchase events in "records"
# Update friends for each befriend/unfriend event
# Save found anomalies in "anomalies"
filename = os.path.join(parent_path, 'log_input' ,'stream_log.json')
with open(filename, 'r') as f:
    for line in f:
        if line.strip(): # to avoid empty lines
            update = json.loads(line,object_pairs_hook=OrderedDict)
            if update['event_type'] == 'purchase':
                update['amount'] = float(update['amount'])
                UpdateAnomalies(anomalies,update,friends,records,D,T)
                del update['event_type']
                records.append(update)
            elif update['event_type'] == 'befriend' or update['event_type'] == 'unfriend':
                UpdateFriends(friends,update)
	    else:
		print('Unrecognized event type \"'+update['event_type']+'\". Skipping line')

# Write flagged_purchases.json
filename = os.path.join(parent_path, 'log_output' ,'flagged_purchases.json')
with open(filename, 'w') as f:
    for anomaly in anomalies:
        anomaly['amount'] = format(anomaly['amount'], '.2f')
        anomaly['mean'] = format(anomaly['mean'], '.2f')
        anomaly['sd'] = format(anomaly['sd'], '.2f')
        json.dump(anomaly,f)
        f.write('\n')