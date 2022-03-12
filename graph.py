import pandas as pd
import numpy as np
import random
class Graph():
    def __init__(self,df):
        self.df = df
        self.query = 0

    def get_sub_graph(self, query, k):
        check = self.df["numeric_id_1"]
        nodes = []
        nodes.append(query)
        # random walk w/ restart
        groups = self.df.groupby("numeric_id_1")
        end = True
        while len(nodes) < k:
            end = True
            curr = query
            while curr in nodes and end:
                selected = groups.get_group(curr)["numeric_id_2"].tolist()
                ind = random.choice(selected)
                if ind not in self.df["numeric_id_1"].unique():
                    end = False
                curr = ind
            if end:
                nodes.append(curr)
            print(len(nodes))
        return nodes




    def sample(self, query):
        #greedy node deletion
        sub = self.get_sub_graph(query, 50)




import pandas as pd

df = pd.read_csv("lib/datasets/twitch_gamers/large_twitch_edges.csv")
tmp = Graph(df)
tmp.sample(1)