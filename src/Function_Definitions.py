import numpy as np
from collections import OrderedDict

# Function Definitions for Anomaly Detection Code

def UpdateFriends(friends,update):
    # friends[key] is the list of friends of customer key
    # update is the required change to friends
    id1 = update['id1']
    id2 = update['id2']
    if update['event_type'] == 'befriend':
        if id1 in friends: 
            friends[id1].append(id2)
        else:
            friends[id1] = [id2]
        if id2 in friends: 
            friends[id2].append(id1)
        else:
            friends[id2] = [id1]
    elif update['event_type'] == 'unfriend':
        if id1 in friends and id2 in friends[id1]:
            friends[id1].remove(id2) 
            friends[id2].remove(id1)
    return

def ReturnFriends(ID,friends,D):
    # Used internally within CheckIfAnomaly
    # Finds the friends list for customer ID
    # See UpdateAnomalies for input description
    if ID in friends:
        friends_list = friends[ID][:]
    else: 
        return set()
    start = 0
    end = len(friends_list)
    d = 1
    while d<D:
        for Id in friends_list[start:end]:
            friends_list.extend(friends[Id][:])
        start = end
        end = len(friends_list)
        d += 1 
    return set(friends_list)-set([ID])

def CheckIfAnomaly(update,friends,records,D,T):
    # Used internally within UpdateAnomalies
    # Checks if update is an anomaly
    # See UpdateAnomalies for input description
    friends_set = ReturnFriends(update['id'],friends,D) 
    L_rec = len(records)
    back_count = 1
    amount_list = []
    while len(amount_list)<T and back_count<=L_rec: 
        # iterate from the most recent purchase
        if records[-back_count]['id'] in friends_set:
            amount_list.append(records[-back_count]['amount'])
        back_count += 1
    # check if enough historical data
    if len(amount_list)<2:
        check = False
        mean = 0
        sd = 0
    # check if anomaly
    else:
        mean = np.mean(amount_list) 
        sd = np.std(amount_list)
        check = float(update['amount'])>mean+3.0*sd
    return check,mean,sd

def UpdateAnomalies(anomalies,update,friends,records,D,T):
    # anomalies is the list of anomalies
    # update is the new purchase record
    # friends is the friends network
    # records is the collected purchase history
    # D is number of degrees of friends
    # T is the tracked number of purchases
    check,mean,sd = CheckIfAnomaly(update,friends,records,D,T)
    if check:
        update['mean'] = mean
        update['sd'] = sd
        anomalies.append(OrderedDict(update))
    return