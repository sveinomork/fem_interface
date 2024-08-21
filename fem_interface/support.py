from fem_interface.fem.fem import FEM
import math
import numpy as np

#from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
#from sklearn import metrics



def read_sestra(file:str,sup_id:int)->dict[int,list[float]]:
    in_dict=dict()
    with open(file, 'r') as f1:
        for line in f1:
            data=line.split()
            if len(data)==4:
                if data[0].strip()==str(sup_id):
                    if int(float(data[2])) not in in_dict:
                        in_dict[int(float(data[2]))]=[]
                    in_dict[int(float(data[2]))].append(float(data[3]))  
    return in_dict 
                    
def get_sum_force(conv_dict:dict[int,float],res_dict:dict[int,float],nodes:list[int],lc:int)->float:
        
        
        t_list=[]
        for k,v in res_dict.items():
            if k not in conv_dict:
                print(f'{k} not in')
                continue
            if int(conv_dict[k]) in nodes:
                t_list.append(v[lc-1])
        return sum(t_list)  

def _get_coordinates(nodes:int):
    o_dict=[]
    nod=[]
    for node in nodes:
        o_dict.append(np.array([node[0],node[1]]))
        nod.append(node[2])

    return o_dict,nod

"""
def automatic_grouping_of_point(nodes,max_dist:float)->dict[int,list[int]]:
    coordinates,nodes=_get_coordinates(nodes)
    
    print(len(nodes))
    clustering= DBSCAN(eps=max_dist, min_samples=1).fit(coordinates)
    labels = clustering.labels_
    print(set(labels))
    print(len(labels))
    grouped_nodes = {}
    for label,node in zip(labels,nodes):
        if label not in grouped_nodes:
            grouped_nodes[label]=[]
            grouped_nodes[label].append(node)
            continue
        grouped_nodes[label].append(node)

        
    
    return grouped_nodes
    
"""
def combine_force(conv_dict:dict[int,float],res_dict_init:dict[int,float],res_dict_tot:dict[int,float],nodes:list[int])->float:
    force_in=get_sum_force(conv_dict,res_dict_init,nodes,1)
    force_tot_1=get_sum_force(conv_dict,res_dict_tot,nodes,1)
    force_tot_2=get_sum_force(conv_dict,res_dict_tot,nodes,2)
    return  force_in+force_tot_2-force_tot_1

def calc_support_reaction(fem_obj:FEM,res_dict_init:dict[int,float],res_dict_tot:dict[int,float],nodes:list[int])->float:
    conv_dict={v.nodex:k for k,v in fem_obj.gnode.items()}
    return combine_force(conv_dict,res_dict_init,res_dict_tot,nodes)


import pickle
def save_obj(obj,name:str)->None:
    with open(f'{name}', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)