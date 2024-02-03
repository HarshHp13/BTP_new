from collections import deque
from math import *
import simulation_parameters as sp
import start as st

Nodes=[]
visited=[]
ex_energy=0
ex_data=0
ex_lat=0
class Node:
    def __init__(self, id,energy, e_tr, e_re, e_th, location, packet_size, data, data_per_cycle, energy_per_cycle) -> None:
        self.id=id
        self.location=location
        self.energy=energy
        self.e_tr=e_tr
        self.e_re=e_re
        self.e_th=e_th
        self.packet_size=packet_size
        self.data_queue=deque()
        self.data_per_cycle=data_per_cycle
        self.eny_per_cycle=energy_per_cycle
    
    def __sub__(self, other):
        return sqrt((self.location[0]-other.location[0])**2+(self.location[1]-other.location[1])**2)
    
    def transmit(self,data,target):
        global ex_energy
        global ex_lat
        ex_lat+=data/sp.data_rate
        self.energy-= ceil(data/self.packet_size)*self.e_tr
        # print("transmit->Node: ",self.id," Next: ",target.id, "eny: ",ceil(data/self.packet_size)*self.e_tr, "data: ",data)
        ex_energy+= ceil(data/self.packet_size)*self.e_tr
        target.reception(data)
        
    def reception(self,data):
        global ex_energy
        # print("reception->Node: ",self.id, "eny: ",ceil(data/self.packet_size)*self.e_tr, "data: ",data )
        self.energy-= ceil(data/self.packet_size)*self.e_re
        ex_energy+= ceil(data/self.packet_size)*self.e_re
        
    def process(self):
        global ex_energy
        global ex_data
        global ex_lat
        tmp= ceil(self.data_queue[0]/self.data_per_cycle)*self.eny_per_cycle
        if(tmp<=self.energy-self.e_th):
            self.energy-=tmp
            ex_energy+=tmp
            ex_data+=self.data_queue[0]
            ex_lat+=ceil(self.data_queue[0]/self.data_per_cycle)/sp.cycles_per_second
            self.data_queue.popleft()
            return True
        else :
            return False
        
    def discover(self,G):
        global ex_energy
        # self.data_queue.popleft()
        min_eny=float("inf")
        flag=True
        nxt_node=-1
        tmp_nxt_node=-1
        min_dist=float("inf")
        for node in G[self.id]:
            if Nodes[node].id==0:
                nxt_node=node
                flag=False
                break
            if(Nodes[node].energy-Nodes[node].e_th>min_eny):
                temp_eny=ceil(self.data_queue[0]/Nodes[node].data_per_cycle)*Nodes[node].eny_per_cycle
                if(temp_eny<=Nodes[node].energy-Nodes[node].e_th):
                    min_eny=temp_eny
                    flag=False
                    nxt_node=node
            if(min_dist>self-Nodes[node] ):
                min_dist=self-Nodes[node]
                tmp_nxt_node=node
        if(flag):
            return [tmp_nxt_node,False]
        else:
            return [nxt_node,True]
        
    def feedback(self,start,G):
        global ex_energy
        global ex_lat
        v=[False for _ in range(len(G))]
        q=deque()
        q.append(start)
        v[start]=True
        while((len(q)>0)):
            node=q.popleft()
            if(node == 0):
                break
            for i in G[node]:
                if(v[i]==False):
                    q.append(i)
                    v[i]=True
                    Nodes[node].transmit((10*1024*8),Nodes[i])
                    ex_lat+=(10*1024*8)/sp.data_rate
            
            
def start(G,E,D,L):
    global ex_data
    global ex_energy
    global ex_lat
    res=[]
    Nodes.append(Node(0,E[0],0,0,0,[0,0],sp.packet_size,0,sp.data_per_cycle,sp.energy_per_cycle))
    for i in range(1,len(G)):
        Nodes.append(Node(i,E[i],sp.e_tr,sp.e_re,sp.e_th,L[i],sp.packet_size,0,sp.data_per_cycle,sp.energy_per_cycle))
    
    for j,data in enumerate(D):
        for i,d in enumerate(data):
            Nodes[i].data_queue.append(d*1024*8)
        for i in range(1,len(G)):
            # visited=[False for _ in range(len(G))]
            # print("Node: ",i,": ", Nodes[i].data_queue[0])
            
            if Nodes[i].process():
                Nodes[i].feedback(i,G)
            
            else:
                nxt_node,flag=Nodes[i].discover(G)
                Nodes[i].transmit(Nodes[i].data_queue[0],Nodes[nxt_node])
                # if(nxt_node==-1):
                #     continue
                # print("Node: ",i," Next: ",nxt_node, "data: ",Nodes[i].data_queue[0])
                cnt=0
                while flag==False and cnt<len(G):
                    next_node,flag=Nodes[nxt_node].discover(G)
                    Nodes[nxt_node].transmit(Nodes[i].data_queue[0],Nodes[next_node])
                    nxt_node=next_node
                    cnt+=1
                if flag:
                    ex_data+=Nodes[i].data_queue[0]
                    if nxt_node==0:
                        continue
                    Nodes[nxt_node].process()
                    Nodes[nxt_node].feedback(nxt_node,G)
                
                
        res.append([ex_data,ex_energy,ex_lat])
        ex_data=0
        ex_energy=0
        ex_lat=0
        
    Nodes.clear()
    return res

def run():
    print("Starting the simulation...")
    G=st.generate(100, 1)
    res=start(G.adj_list,G.energy,G.data,G.location)
    for ind,i in enumerate(res):
        print(ind,":",i[0],i[1],i[2],i[0]/(i[1]+i[2]))
        