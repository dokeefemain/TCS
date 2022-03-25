# TCS: Twitch Channel Suggestions

## Overview
The purpous of this project is to be able to suggest a Twitch user 5 streamers they might like to watch using Suggestion Algorithms. More specifically it uses Random Walk with Restart, Personalized Page Rank, HITS and SALSA in a manner that is similar to Twitters WTF algorithm.

## Dataset
The dataset used is Twitch Gamers. It contains 6 million different directed edges that represent the user to user follow relationship. For those who aren't aware of Twitch it's graph structure is the same as Twitters.

##  Sampling
One of the bigger issues I encountered in this was the size of the data set. For PPR(Personalized Page Rank) if you didn't sample the data your PC would need to be capable of holding a 6,000,000 x 6,000,000 matrix and with 16gb of ram that isn't possible.

Sampling social network graphs can be pretty tricky since you want to be able to preserve stuff like the node degree distribution. The method that I used to do this is Random Walk with Restart. Since we only care about suggestions for one user this method makes the most sense.

There is an issue with this though. I need a large amount of data and RWR slows down significantly after you have identified around 150 nodes. Once that happens I just randomly select another node and run RWR again. 

## Algorithms

### WTF
WTF is Twitters Who To Follow algorithm. Is basically an implementation of the SALSA algorithm. As I stated before the Twitch social network graph is basically the same as Twitter. So I figured it would be a good choice to use.

### SALSA
The SALSA algorithm is a link suggestion algorithm what was developed in the early 2000's. At the time the 2 main algorithms where PageRank and HITS. SALSA basically combines both of these. 

SALSA can be broken down into a couple steps. Firstly you do an egocentric random walk(PPR) around your query node. This alone is a good enough suggestion algorithm but they take it a step further. Now they run HITS algorthm on those nodes by treating them as Hub nodes then the Authority nodes are the nodes that the hub nodes point to. From there you do some linear algebra and then solve for eigen vectors and you have your suggested users.

All of this has been implemented in lib/salsa.py and you can see an example usage in TCS_Salsa.ipynb
