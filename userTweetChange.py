import os
import pickle
import gc

roundList = ['round1', 'round2', 'round3', 'round4', 'round5', 'round6', 'round7', 'round8', 'round10', 'round11', 'round12', 'round13', 'round14', 'round15']
currDir = '/media/EXTHDD/UnfollowData/WeeklySnapshots/round1-15/'
outputDir = '/media/EXTHDD/UnfollowData/WeeklySnapshots/round1-15/'


index = 0
while index < (len(roundList) - 1):
    count = 0
    print("working on " + roundList[index] + " and " + roundList[index + 1])

    #open the files
    dicti = {}
    for i in os.listdir(os.path.join(currDir, roundList[index], 'Tweets')):        
        if os.path.isfile(os.path.join(currDir, roundList[index + 1], 'Tweets', i)):
            with open(os.path.join(currDir, roundList[index], 'Tweets', i), 'rb') as r1:
                with open(os.path.join(currDir, roundList[index + 1], 'Tweets', i), 'rb') as r2:
                    #load files
                    firstRound = pickle.load(r1)
                    secondRound = pickle.load(r2)

                    #find all keys
                    firstKeys = set()
                    secondKeys = set()
                    if index==0:
                        firstRound=firstRound[0]
                    for j in firstRound:
                        firstKeys.add(j['id'])
                    for k in secondRound:
                        secondKeys.add(k['id'])
                    #print(secondKeys - firstKeys)
                    #print(firstKeys - secondKeys)

                    user_id = int(i.split('_')[0])
                    # print(user_id)
                    dicti[user_id] = [secondKeys - firstKeys, firstKeys - secondKeys]
                    if count % 1000 == 0:
                        print(count)
                    count += 1

    file_name = str(roundList[index]) + str(roundList[index + 1]) + "Change.pkl"
    open_file = open(os.path.join(outputDir, "UserTweetChange", file_name), "wb")
    pickle.dump(dicti, open_file)
    open_file.close()
    gc.collect()
    index = index + 1
