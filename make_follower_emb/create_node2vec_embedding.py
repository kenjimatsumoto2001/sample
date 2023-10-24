# node2vecの学習モデルを作成
from node2vec import Node2Vec
import networkx as nx

class Node2vec_Embedding:
    def __init__(self, graph: nx.Graph, dimensions: int = 128, walk_length: int = 80, num_walk: int = 10, p: float = 1,
                 q: float = 1, file_label: str = "test", sg: int = 1, file_pass: str="./embeddings_new/"):
        self.G = graph
        self.dimensions = dimensions
        self.walk_length = walk_length
        self.num_walk = num_walk
        self.p = p
        self.q = q
        self.file_label = file_label
        self.sg = sg #sg=1: skip-gram, sg=0: cbow
        self.emb_name = self.mk_emb_name() #ファイル名
        #self.file_pass = file_pass

        #EMBEDDING_FILENAME = './embeddings/' + self.emb_name + '.emb'
        #EMBEDDING_MODEL_FILENAME = './embeddings/' + self.emb_name + '.model'
        EMBEDDING_FILENAME = file_pass + self.emb_name + '.emb'
        EMBEDDING_MODEL_FILENAME = file_pass + self.emb_name + '.model'
        
        print(EMBEDDING_MODEL_FILENAME)
        
        #### walk_lengthが一回のウォークのノード数、num_walksが１つのノードから何回ウォークを行うか
        node2vec = Node2Vec(self.G, dimensions=dimensions, walk_length=walk_length, num_walks=num_walk, p=p, q=q, workers=4)
        model = node2vec.fit(window=10, min_count=1, sg = sg, batch_words=4) #sg = 1はskip-gram, その他はcbow

        #### 保存しないときはコメントアウト
        model.wv.save_word2vec_format(EMBEDDING_FILENAME)
        model.save(EMBEDDING_MODEL_FILENAME)

    ### 保存するファイル名を作成
    def mk_emb_name(self):
        #### p, qは小数の場合，小数点を消した文字列に変換する ex.) 0.1 -> 01
        emb_name = "{}_{}_{}_{}_{}_{}_sg0{}_{}".format("embeddings", self.dimensions, self.walk_length, self.num_walk, str(self.p).replace(".", ""), str(self.q).replace(".", ""), self.sg, self.file_label)
        return emb_name

if __name__ == '__main__':
    import get_service_data as gsd
    import create_network
    import pprint
    """
    mashup_pass = "./json/mashup_data.json"
    gm = gsd.Get_Mashup(mashup_pass)
    mashup_dict = gm.get_all_mashup_apis()
    
    cn = create_network.Create_Network()
    cn.mk_renkei_dict(mashup_dict)
    G = cn.mk_simple_graph()

    diminsions = 4
    walk_length = 30
    num_walk = 200
    p = 0.1
    q = 0.6
    file_label = "test"

    ne = Node2vec_Embedding(G, diminsions, walk_length, num_walk, p, q, file_label)
    """
    #sample
    dict_data = {"x": ["1", "2"], "y": ["2", "3"], "z": ["1", "3", "4"], "1":["x", "z"], "2":["x","y"], "4":["z"]}
    cn = create_network.Create_Network()
    cn.mk_renkei_dict(dict_data)
    G = cn.mk_simple_graph()
    
    file_name = "dousa_test"
    mn = Node2vec_Embedding(G, 4, 5, 2, 0.1, 0.6, file_name, 1)
    print(mn.emb_name)
    
    