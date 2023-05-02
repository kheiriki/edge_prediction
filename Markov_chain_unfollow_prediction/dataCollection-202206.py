import os
import pickle
import gc
currDir = '/home/jack/unfollow_project/unfollower-2022-5'

# f = open(os.path.join(currDir, "megaUserSet.pkl"), 'rb')
# megaUserSet = pickle.load(f) # user set
# f.close()
# print("Mega User set loaded.")

# g = open(os.path.join(currDir, "megaTweetSet.pkl"), 'rb')
# megaTweetSet = pickle.load(g) # all tweet in set
# g.close()
# print("Mega Tweet set loaded.")

# file_name = "output.txt"
# output = open(file_name, "w")

# for filename in os.listdir('/home/jack/unfollow_project/unfollower-2022-5/UserTweetChange'):
#     with open(os.path.join('/home/jack/unfollow_project/unfollower-2022-5/UserTweetChange', filename), 'rb') as f:
#         file = pickle.load(f)
#         for i in file: # for all tweet set
#             for tweetID in file[i][0]: # for all tweets
#                 output.write(str(i) + ' ' + str(tweetID) + '\n')
#                 for m in megaTweetSet[tweetID]['mention_user_id']:
#                     if m['id'] in megaUserSet:
#                         output.write(m['id_str'] + ' ' + str(tweetID) + '\n')


# output.close()


##### batch 2 - zero-indexed data
# file_name = "output.txt"
# temp = open(file_name, "r")
# file2 = "output2.txt"
# output = open(file2, 'w')
# userSet = {}
# tweetSet = {}
# userCount = 0
# tweetCount = 0

# while True:
#     # Get next line from file
#     line = temp.readline()
#     if not line:
#         break

#     line = line.strip('\n').split(' ')
#     userID = line[0]
#     tweetID = line[1]

#     if userID not in userSet.keys():
#         userSet[userID] = userCount
#         userCount += 1
#     if tweetID not in tweetSet.keys():
#         tweetSet[tweetID] = tweetCount
#         tweetCount += 1

#     output.write(str(userSet[userID]) + ' ' + str(tweetSet[tweetID]) + '\n')

# temp.close()
# output.close()

#### batch3 - no repetition zero-indexed data
file_name = "output2.txt"
temp = open(file_name, "r")
file2 = "output3.txt"
output = open(file2, 'w')
tupleSet = set()

while True:
    # Get next line from file
    line = temp.readline()
    if not line:
        break

    line = line.strip('\n').split(' ')
    userID = line[0]
    tweetID = line[1]

    if tuple([userID, tweetID]) not in tupleSet:
        tupleSet.add(tuple([userID, tweetID]))
        output.write(str(userID) + ' ' + str(tweetID) + '\n')

temp.close()
output.close()