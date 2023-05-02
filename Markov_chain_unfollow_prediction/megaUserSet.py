import os
import pickle

currDir = '/media/EXTHDD/UnfollowData/WeeklySnapshots/round1-15/FriendFollowerChange/'
output = set()
for filename in os.listdir(currDir):
    print(filename)
    with open(os.path.join(currDir, filename), 'rb') as f:
        print("opening data set " + filename)
        dicti = pickle.load(f)
        # print(dicti.keys())
        if len(output) == 0:
            #print(set(list(dicti.keys())))
            output = set(dicti.keys())
            #print(output)
        output = output.intersection(set(dicti.keys()))
        print("...finishing data set " + filename)


file_name = "/media/EXTHDD/UnfollowData/WeeklySnapshots/round1-15/megaUserSet.pkl"
open_file = open(file_name, "wb")
pickle.dump(output, open_file)
print(output)
open_file.close()
