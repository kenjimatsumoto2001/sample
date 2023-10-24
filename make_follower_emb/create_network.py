# ネットワークを作成
import networkx as nx
import pprint

class Create_Network:
    def __init__(self):
        self.renkei_dict = dict()
    
    ### {サービス名：[連携したことのあるサービスリスト]}の辞書データを作成
    def mk_renkei_dict(self, mashup_dict: dict = None) -> dict:
        renkei_dict = dict()
        num = 0
        for apis in mashup_dict.values():
            for api in apis:
                if api not in renkei_dict:
                    renkei_dict[api] = list()
                renkei_dict[api].extend(apis)
                num += 1
                #print(num)
        
        renkei_dict2 = dict()
        for k, v in renkei_dict.items():
            v = list(set(v))
            if k in v:
                v.remove(k)
            renkei_dict2[k] = v
        self.renkei_dict = renkei_dict2
        return renkei_dict2

    ### ノードリストの作成
    def mk_nodes_list(self) -> list:
        return [key for key in self.renkei_dict.keys()]

    ### エッジリストの作成
    def mk_edges_list(self) -> list:
        edges_list = list()
        for key, values in self.renkei_dict.items():
            edges_list.extend([[key, v] for v in values])
        return edges_list

    ### 双方向エッジデータを一方向にするメソッド．単純無向グラフでは強制的に一方向にされるのでいらない
    def filter_edges(self, edges_list: list = None) -> list:
        result = list()
        for edge in edges_list:
            if [edge[1], edge[0]] not in result:
                result.append(edge)
        return result

    ### 単純無向グラフの作成
    def mk_simple_graph(self) -> nx.Graph:
        G = nx.Graph()
        ##### ノードはエッジ作成時に自動生成されるのでいらない
        #nodes_list = self.mk_nodes_list()
        #G.add_nodes_from(nodes_list)
        edges_list = self.mk_edges_list()
        G.add_edges_from(edges_list)
        print("ノード数：{}  /  エッジ数：{}".format(nx.number_of_nodes(G), nx.number_of_edges(G)))

        #test = nx.shortest_path(G, target="google_maps")
        #for key, val in test.items():
            #if len(val) < 2:
                #print(key, val)
        return G


if __name__ == '__main__':
    import get_service_data as gsd

    mashup_pass = "./json/mashup_data.json"
    gm = gsd.Get_Mashup(mashup_pass)
    mashup_dict = gm.get_all_mashup_apis()
    
    cn = Create_Network()
    cn.mk_renkei_dict(mashup_dict)
    cn.mk_simple_graph()
