import pprint
import time
# 隣接データを作成する
def mk_relate_network(mashup_dict):
    relate_network = dict()
    for val_list in mashup_dict.values():
        for val in val_list:
            if val in relate_network:
                relate_network[val].extend(val_list)
            else:
                relate_network[val] = val_list

    for key, val in relate_network.items():
        val = list(set(val))
        val.remove(key)
        relate_network[key] = val
    print(relate_network)
    return relate_network
    

if __name__=='__main__':
    start = time.time()
    #jsonファイルからマッシュアップ，サービスデータを取得
    import get_service_data
    mashup_pass = "./json/mashup_data_new.json"
    api_pass = "./json/api_data_new.json"
    get_mashup = get_service_data.Get_Mashup(mashup_pass)
    get_api = get_service_data.Get_Api(api_pass)
    
    mashup_dict = get_mashup.get_all_mashup_apis()
    api_dict = get_api.get_all_api_category()
    relate_network = mk_relate_network(mashup_dict) #{ サービス名：隣接サービス }，ネットワークの構築方法によっては相互リンクになるので注意
    
    #説明文があるapiをフィルタリングする，bertと要素数を同じにするときに使う
    api_names_fileter = [row for row in relate_network.keys() if get_api.get_describe(row) != "no_describe"]
    
    #ネットワークの生成
    import create_network
    cn = create_network.Create_Network()
    cn.mk_renkei_dict(mashup_dict)
    print(cn)
    #exit()
    G = cn.mk_simple_graph()
    
    
    #学習モデルの生成
    import create_node2vec_embedding
    #nums = [50,200]
    nums = [100]
    for i in nums:
        diminsions = 8
        walk_length = i
        num_walk = 50
        p = 0.1
        q = 0.6
        file_label = "skip"
        sg = 1 #sg = 1はskip-gram, その他はcbow
        ne = create_node2vec_embedding.Node2vec_Embedding(G, diminsions, walk_length, num_walk, p, q, file_label, sg)
        emb_name = ne.emb_name #モデル名
        
        #print("write csv file")
        #csvへの書き込み
        #実行後は処理時間がかかるのでコメントアウト
        import col_node2vec
        import operate_csv
        file_name = emb_name #学習モデル生成をコメントアウトしてない時は，こっち使う
        #file_name = "original_walks_4_60_200" #その他のファイル名
        
        cln = col_node2vec.Col_Node2vec(file_name)
        #api_name_list = [key for key in relate_network.keys()]
        api_name_list = api_names_fileter
        #カラムの生成
        columns = ["api_name"]
        columns.extend(api_name_list)
        result_list = list()
        result_list.append(columns)

        #総当たり類似度行データの生成
        for api1 in api_name_list:
            simillar_list = [cln.sim_word1_word2(api1, api2) for api2 in api_name_list]
            simillar_list.insert(0, api1)
            result_list.append(simillar_list)

        write_csv_file = file_name
        #csv操作
        csv_pass = "./csv_new/" + write_csv_file + ".csv"
        op_csv = operate_csv.Op_Csv()
        op_csv.write_csv(result_list, csv_pass) #csvへの書き込み
        #num作る
        import sakujo
        csv_pass_num = "./csv_new/" + write_csv_file + "_num.csv" 
        sk = sakujo.Sakujo()
        sk.del_gyou_retu(csv_pass, csv_pass_num)
        print(time.time() - start)



    """
    #k-meansクラスタリング
    import create_cluster
    n_clusters = 119
    #simillar_csv = "embeddings_4_30_200_01_06_test"
    simillar_csv = "embeddings_4_30_200_01_06_sg01_No1"
    clustering = create_cluster.Clustering("./csv/"+simillar_csv+".csv", "./csv/"+simillar_csv+"_num.csv")
    cluster_dict, similarities, cluster_labels = clustering.k_clustering(n_clusters)
    
    #purityの計算
    import col_purity
    N = 1339
    n2v_purity = col_purity.Purity(mashup_dict, api_dict)
    correct_cluster = n2v_purity.mk_correct_cluster()
    
    n2v_purity_val = n2v_purity.col_purity(cluster_dict, correct_cluster, N)
    print("node2vec：{}".format(n2v_purity_val))
    """
    
