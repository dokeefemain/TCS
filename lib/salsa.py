import networkx as nx
import pandas as pd
import numpy as np
from networkx.algorithms import bipartite
from networkx.algorithms.bipartite.matrix import biadjacency_matrix
class Salsa(object):
    def __init__(self, path):
        self.df = pd.read_csv(path)
        self.g = nx.from_pandas_edgelist(self.df, source='numeric_id_1', target="numeric_id_2", edge_attr=None, create_using=nx.DiGraph())
        self.query = 1
        self.stationary = []
        self.auth = []
        self.suggestions = []

    def top_k_suggestions(self, num):
        idx = (-self.stationary).argsort()[:num]
        # Top 5 Predicted channels
        suggestions = np.array(self.auth)[idx]
        self.suggestions = suggestions
        print("Suggested channels are:", suggestions)
        print("Shortests paths:")
        for i in suggestions:
            try:
                print(nx.shortest_path(self.g, source=self.query, target=i))
            except:
                print("No path between",self.query,"and",i)

    def set_query(self, query):
        self.query = query



    def salsa(self):
        personal = {}
        for i in range(self.g.number_of_nodes()):
            if i == self.query:
                personal[i] = self.query
            else:
                personal[i] = 0
        # computing PPR
        ppr = nx.pagerank(self.g, personalization=personal)
        top_ppr = sorted(ppr, key=ppr.get, reverse=True)[:200]
        tmp = []
        tmp1 = []
        idk = self.df["numeric_id_1"].unique()
        for i in top_ppr:
            if i in idk:
                tmp.append("Hub " + str(i))
                tmp1.append(i)
        con_ppr = tmp1
        unique = []
        for i in con_ppr:
            group = self.df[self.df.numeric_id_1 == i]["numeric_id_2"]
            for j in group:
                unique.append(j)
        unique = list(set(unique))

        #getting connected components
        b = nx.Graph()
        b.add_nodes_from(tmp, bipartite=0)
        b.add_nodes_from(unique, bipartite=1)
        for i in range(len(con_ppr)):
            group = self.df[self.df.numeric_id_1 == con_ppr[i]]["numeric_id_2"]
            for j in group:
                b.add_edge(tmp[i], j)
        test = True
        tmp = []
        hubs = []
        auth = []
        for i in nx.connected_components(b):
            if test:
                test = False
                for j in i:
                    if type(j) == str:
                        hubs.append(j)
                    else:
                        auth.append(j)
        self.auth = auth
        bi = nx.Graph()
        bi.add_nodes_from(hubs, bipartite=0)
        bi.add_nodes_from(auth, bipartite=1)
        for i in hubs:
            curr = int(i[4:])
            group = self.df[self.df.numeric_id_1 == curr]["numeric_id_2"]
            for j in group:
                bi.add_edge(i, j)

        #Getting adj for the bi graph
        L = biadjacency_matrix(bi, row_order=hubs, column_order=auth).toarray()
        #rows divided by row sums
        Lr = []
        for i in L:
            Lr.append(i / i.sum())
        Lr = np.array(Lr)
        #cols divided by col sums
        Lc = []
        for i in L.T:
            Lc.append(i / i.sum())
        Lc = np.array(Lc)
        A = np.dot(Lc, Lr)

        print("Computing Stationary Matrix")
        evals, evecs = np.linalg.eig(A.T)
        evec1 = evecs[:, np.isclose(evals, 1)]
        evec1 = evec1[:, 0]

        stationary = evec1 / evec1.sum()
        self.stationary = stationary.real

