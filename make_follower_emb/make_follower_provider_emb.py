import os
import get_service_data
import pickle
from itertools import islice

def dict_chunks(data, size):

    it = iter(data)

    for i in range(0, len(data), size):

        yield {k:data[k] for k in islice(it, size)}

def mk_relate_network(mashup_dict):
    num = 0
    relate_network = dict()
    for val_list in mashup_dict.values():
        num += 1
        print(num)
        #print(val_list)
        for val in val_list:
            if val in relate_network:
                relate_network[val].extend(val_list)
            else:
                relate_network[val] = val_list
            
    
    for key, val in relate_network.items():
        val = list(set(val))
        val.remove(key)
        relate_network[key] = val
        #print(val)
    
    return relate_network
    
api_pass = "./json/api_data_new.json"
get_api = get_service_data.Get_Api(api_pass)
path = "./api_follower"
files = os.listdir(path)
all_dic = {}
for i in files:
    f = open(path + "/" + i)
    f = f.readlines()
    i = i.replace("_follower.txt","")
    provider = get_api.get_privider(i)
    provider = provider[0]
    #print(provider)
    followers = []
    for j in f:
        j = j.replace("\n","")
        followers.append(j)

    if provider in all_dic:
        if followers == []:
            pass
        else:
            if all_dic[provider] == None:
               all_dic[provider] = followers 
            else:
                #print(all_dic[provider])

                ts = all_dic[provider]
                for l in followers:
                    ts.append(l)
                all_dic[provider] = ts
                #print(all_dic[provider])
                
    else:
        if followers == []:
            pass
        else:
            all_dic[provider] = followers
#print(all_dic)
#print(len(all_dic))
#exit()
"""
chunks = dict_chunks(all_dic, size=1000)
n = 0
for c in chunks:

    with open("dicts/myDictionary_" + str(n) + ".txt", "wb") as tf:
        pickle.dump(c,tf)
    n += 1
"""
#exit()
#print(all_dic["google"])
#print(len(all_dic))
#crelate_network = mk_relate_network(all_dic) 
#print(relate_network)
import create_network
cn = create_network.Create_Network()


cn.mk_renkei_dict(all_dic)
print("clear_1")
G = cn.mk_simple_graph()
print("clear_2")


import create_node2vec_embedding
#nums = [50,200]
nums = [1]
for i in nums:
    diminsions = 1
    walk_length = i
    num_walk = 5
    p = 0.1
    q = 0.6
    file_label = "skip"
    sg = 1 #sg = 1はskip-gram, その他はcbow
    ne = create_node2vec_embedding.Node2vec_Embedding(G, diminsions, walk_length, num_walk, p, q, file_label, sg)
    emb_name = ne.emb_name #モデル名