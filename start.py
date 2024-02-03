import random
import numpy as np

cnst = np.random.randint(1000000000)
cnst = 969602876
random.seed(cnst)
np.random.seed(cnst)

class SubGraph:
    def __init__(self, given_nodes, itr, dr, me):
        print(f'got from cnst : {cnst}')
        self.n = given_nodes.size
        self.location = np.random.randint(500, size=(self.n, 2))
        self.energy = me+1*np.random.rand()*np.ones(self.n)
        self.data = np.random.randint(dr[0],dr[1], size=(itr, self.n))
        self.adj_list = [[] for _ in range(self.n)]
        self.edges = []
        self.nodes = given_nodes
        nodes = np.arange(self.n)
        while(nodes.size > 1):
            np.random.shuffle(nodes)
            ind = np.arange(1, nodes.size, 2)-1
            for i in ind:
                if nodes[i] < nodes[i+1]:
                    self.edges.append([nodes[i], nodes[i+1]])
                else:
                    self.edges.append([nodes[i+1], nodes[i]])
                self.adj_list[nodes[i]].append(nodes[i+1])
                self.adj_list[nodes[i+1]].append(nodes[i])
            if nodes.size%2 == 1:
                ind = np.append(ind, [nodes.size-1])
            nodes = nodes[ind]
        for i in range(self.n+int(self.n/5)):
            x = np.random.randint(self.n-1)
            y = np.random.randint(x+1, self.n)
            if [x, y] not in self.edges:
                self.edges.append([x, y])
                self.adj_list[x].append(y)
                self.adj_list[y].append(x)
        
    def __str__(self):
        return str(self.edges)

def generate(n,dr,me,itr):
    nodes = np.arange(n)
    g = SubGraph(np.array(nodes), itr, dr, me)
    g.energy[0]=float("inf")
    g.energy=g.energy.tolist()
    g.data=g.data.tolist()
    g.location=g.location.tolist()
    # for i, al in enumerate(g.adj_list):
    #     print(g.nodes[i], g.nodes[al])
    return g

# g = generate(4, 4)
# print(g)