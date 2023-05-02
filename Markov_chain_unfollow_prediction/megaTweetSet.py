import os
import pickle

roundList = ['round1','round2', 'round3', 'round4', 'round5', 'round6', 'round7', 'round8', 'round9', 'round10', 'round11', 'round12', 'round13', 'round14', 'round15']
currDir = '/media/EXTHDD/UnfollowData/WeeklySnapshots/round1-15/'

megaUserSet = {}
with open("/media/EXTHDD/UnfollowData/WeeklySnapshots/round1-15/megaUserSet.pkl", 'rb') as f:
    megaUserSet = pickle.load(f)
print("1")

megaTweetSet = {}

for roundName in roundList:
    print("...processing " + roundName)
    keySet = set(megaTweetSet.keys())
    #print(keySet)
    counter = 0

    if os.path.isdir(os.path.join(currDir, roundName,'Tweets')):
        for filename in os.listdir(os.path.join(currDir, roundName, 'Tweets')):
            with open(os.path.join(currDir, roundName, 'Tweets', filename), 'rb') as f:
                dicti = pickle.load(f)
                if roundName=='round1':
                    dicti=dicti[0]
                #print(len(dicti[0]))
                #continue
                user_id = filename.split('_')[0]
                for i in dicti:
                    if i['id'] not in keySet: 
                        t = {'user_id': user_id, 'mention_user_id': i['entities']['user_mentions'], 'text': i['text'],
                             'lang': i['lang']}

                        if 'retweeted_status' in i.keys():  # retweet type
                            if 'quoted_status' in i['retweeted_status'].keys():
                                t['retweet_text'] = i['retweeted_status']['quoted_status']['text']
                                t['retweet_id'] = i['retweeted_status']['quoted_status']['id']
                                t['retweet_lang'] = i['retweeted_status']['quoted_status']['lang']
                            else:
                                t['retweet_text'] = i['retweeted_status']['text']
                                t['retweet_id'] = i['retweeted_status']['id']
                                t['retweet_lang'] = i['retweeted_status']['lang']

                            if t['retweet_id'] in megaUserSet:  # original poster in user set
                                t['type'] = 6
                                t['retweet_user_id'] = i['retweeted_status']['quoted_status']['user']['id']
                            else:  # original poster not in user set
                                t['type'] = 5

                        elif 'quote_status' in i.keys():  # quoted type
                            t['quote_tweet_id'] = i['quote_status']['id']
                            t['quote_text'] = i['quote_status']['text']
                            t['quote_lang'] = i['quote_status']['lang']
                            if i['quoted_status']['user']['id'] in megaUserSet:  # original poster in user set
                                t['type'] = 4
                                t['quote_user_id'] = i['quoted_status']['user']['id']
                            else:  # original poster not in user set
                                t['type'] = 3

                        else:  # reply
                            if i['in_reply_to_user_id'] in megaUserSet:
                                t['type'] = 2
                                t['reply_user_id'] = i['in_reply_to_user_id']
                            else:
                                t['type'] = 1

                        megaTweetSet[i['id']] = t
                counter = counter + 1
                if counter % 1000 == 0:
                    print(counter)

file_name = "/media/EXTHDD/UnfollowData/WeeklySnapshots/round1-15/megaTweetSet.pkl"
open_file = open(file_name, "wb")
pickle.dump(megaTweetSet, open_file)
open_file.close()
