import os
import pickle
from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')
currDir = '/home/jack/unfollow_project/unfollower-2022-5'
outputDir = '/home/jack/unfollow_project/unfollower-2022-5'

f = open(os.path.join(outputDir, "unfollowDataSet.pkl"), 'rb')
ufSet = pickle.load(f) # all user in set
f.close()
print("Data set loaded.")

g = open(os.path.join(outputDir, "megaTweetSet.pkl"), 'rb')
megaTweetSet = pickle.load(g) # all tweet in set
g.close()
print("Mega Tweet set loaded.")

UnfollowDataPoint = set()
count = 0
wkCount = 27
while wkCount <= 37 and count < 10000:
    ufSet2 = ufSet.copy()
    file1 = "round" + str(wkCount - 3) + "round" + str(wkCount - 2) + "Change.pkl"
    file2 = "round" + str(wkCount - 2) + "round" + str(wkCount - 1) + "Change.pkl"
    file3 = "round" + str(wkCount - 1) + "round" + str(wkCount) + "Change.pkl"
    file4 = "round" + str(wkCount) + "round" + str(wkCount + 1) + "Change.pkl"
    file5 = "round" + str(wkCount + 1) + "round" + str(wkCount + 2) + "Change.pkl"
    f1 = open(os.path.join(currDir,"UserTweetChange",file1), "rb")
    f2 = open(os.path.join(currDir,"UserTweetChange",file2), "rb")
    f3 = open(os.path.join(currDir,"UserTweetChange",file3), "rb")
    f4 = open(os.path.join(currDir,"UserTweetChange",file4), "rb")
    f5 = open(os.path.join(currDir,"UserTweetChange",file5), "rb")

    wk1 = pickle.load(f1)
    wk2 = pickle.load(f2)
    wk3 = pickle.load(f3)
    wk4 = pickle.load(f4)
    wk5 = pickle.load(f5)

    f1.close()
    f2.close()
    f3.close()
    f4.close()
    f5.close()

    wk_list = [wk1, wk2, wk3, wk4, wk5]
    print("loaded week " + str(wkCount))
    for ufPoint in ufSet:
        if count >= 10000:
            break
        if int(ufPoint[3]) == wkCount:
            ufSet2.remove(ufPoint)
            count += 1
            #aggregate tweets for -2 -1 0 1 2 week
            user = int(ufPoint[0])
            uf_user = int(ufPoint[2])

            diff = []
            for c in wk_list:
                userTweetID = c[user][0]
                uf_userTweetID = c[uf_user][0]
                userTweetList = []
                uf_userTweetList = []
                
                # print("user:")
                for i in userTweetID:
                    tweet = megaTweetSet[i]
                    # print("current tweet: " + tweet['text'])
                    userTweetList.append(tweet['text'])
                    if megaTweetSet[i]['type'] > 4 :
                        # print(tweet['retweet_text'])
                        userTweetList.append(tweet['retweet_text'])
                    elif megaTweetSet[i]['type'] > 2 :
                        # print(tweet['quote_text'])
                        userTweetList.append(tweet['quote_text'])
                
                # print("uf:")
                for i in uf_userTweetID:
                    tweet = megaTweetSet[i]
                    # print("current tweet: " + tweet['text'])
                    uf_userTweetList.append(tweet['text'])
                    if megaTweetSet[i]['type'] > 4 :
                        # print(tweet['retweet_text'])
                        uf_userTweetList.append(tweet['retweet_text'])
                    elif megaTweetSet[i]['type'] > 2 :
                        # print(tweet['quote_text'])
                        uf_userTweetList.append(tweet['quote_text'])
                
                if userTweetList == []:
                    diff.append("null")
                elif uf_userTweetList == []:
                    diff.append("null")
                else:
                    mUser = model.encode(userTweetList)
                    mUf = model.encode(uf_userTweetList)
                    dot = util.dot_score(mUser, mUf)
                    mean = torch.mean(dot)
                # print(mean)
                    diff.append(mean)

            UnfollowDataPoint.add(ufPoint + tuple(diff))
            if count % 100 == 0:
                print(count)
                print("dataset size" + str(len(UnfollowDataPoint)))

    wkCount += 1
    ufSet = ufSet2


file_name = "unfollowTweet5Week3.pkl"
open_file = open(os.path.join(outputDir, file_name), "wb")
pickle.dump(UnfollowDataPoint, open_file)
open_file.close()
