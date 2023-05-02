
import glob
from tqdm import tqdm
from cdlib import evaluation
users=glob.glob('round1/Tweets/*')
users=[u.split('/')[-1].split('_')[0] for u in users]
all_users={}
for u in users:
    all_users[int(u)]=int(u)



for round in tqdm(range(1,16)):
	round1_follower_followee= pickle.load(open('aggregatedRounds/round{}FriendFollowers.pkl'.format(round),'rb'))
	g=nx.DiGraph()
	for u in tqdm(round1_follower_followee.keys()):
	    try:
	        h= all_users[int(u)]
	    except:
	        print("no users", u)
	        continue
	    followees =round1_follower_followee[u][0]
	    followers =round1_follower_followee[u][1]
	    for f in list(followees):
	        
	        try:
	            all_users[int(f)]
	            g.add_edge(int(h),int(f))
	        except:            
	            pass
	    for f in followers:
	        try:
	            all_users[int(f)]
	            g.add_edge(int(f),int(h))
	        except:            
	            pass
	with open("community/graph_round{}.pkl".format(round),"wb") as fp:
		pickle.dump(g,fp)

	
