# node2vec学習モデルを用いて類似度など出力
from gensim.models import word2vec

class Col_Node2vec():
    def __init__(self, file_name):
        #ディレクトリ変えるならここ
        self.model = word2vec.Word2Vec.load("./embeddings_new/" + file_name + ".model")
        #以下は読み方変えた
        #self.model = word2vec.KeyedVectors.load_word2vec_format("./experiment_new/embedding_ex_new/" + file_name + ".model")

        #experiment_file = "./experiment/embedding_ex/"
        #self.model = word2vec.Word2Vec.load(experiment_file + file_name + ".model")

    ### api_nameの類似度高い（or低い）順のサービス一覧
    #### reverse=Trueなら降順，Falseなら昇順に類似度を出力する
    def node2vec(self, api_name: str = "google_maps", reverse: bool = True) -> list:
        #### topn = xで出力する数を設定できる，topn=∞の場合，可能な限り出力する
        #### （メモ書き）positiveを複数指定すること可能 ex.) [日本, アメリカ]
        #### （メモ書き）negative=["日本"]でpositive-negativeの類似度高いものを出力
        results_sim = self.model.wv.most_similar(positive=[api_name], topn=10000)
        if reverse == False:
            results_sim = self.sort_simillar({row[0]:row[1] for row in results_sim})
        return results_sim

    ### 出力するサービス名の順番をソートする
    def sort_simillar(self, simillar_dict: dict = None) -> list:
        return sorted(simillar_dict.items(), key=lambda x:x[1], reverse=False)

    ### api_nameのベクトル出力
    def show_vector(self, api_name: str = "google_maps"):
        return self.model.wv[api_name]

    ### api_name1とapi_name2の類似度
    def sim_word1_word2(self, api_name1: str = "google_maps", api_name2: str = "yahoo_maps"):
        return self.model.wv.similarity(api_name1, api_name2)

    def cbow_test(self):
        return self.model.predict_output_word(["google_maps"])
    
    def skip_test(self):
        return self.model.wv.most_similar(["google_maps"])





class Col_Node2vec_SNE():
    def __init__(self, file_name):
        #ディレクトリ変えるならここ
        #self.model = word2vec.Word2Vec.load(file_name + ".emb")
        #self.model = word2vec.Word2Vec.load("./SNE/" + file_name + ".emb") 
        #以下は読み方変えた
        self.model = word2vec.KeyedVectors.load_word2vec_format(file_name + ".emb")

        #experiment_file = "./experiment/embedding_ex/"
        #self.model = word2vec.Word2Vec.load(experiment_file + file_name + ".model")

    ### api_nameの類似度高い（or低い）順のサービス一覧
    #### reverse=Trueなら降順，Falseなら昇順に類似度を出力する
    def node2vec(self, api_name: str = "google_maps", reverse: bool = True) -> list:
        #### topn = xで出力する数を設定できる，topn=∞の場合，可能な限り出力する
        #### （メモ書き）positiveを複数指定すること可能 ex.) [日本, アメリカ]
        #### （メモ書き）negative=["日本"]でpositive-negativeの類似度高いものを出力
        results_sim = self.model.wv.most_similar(positive=[api_name], topn=10000)
        if reverse == False:
            results_sim = self.sort_simillar({row[0]:row[1] for row in results_sim})
        return results_sim

    ### 出力するサービス名の順番をソートする
    def sort_simillar(self, simillar_dict: dict = None) -> list:
        return sorted(simillar_dict.items(), key=lambda x:x[1], reverse=False)

    ### api_nameのベクトル出力
    def show_vector(self, api_name: str = "google_maps"):
        return self.model.wv[api_name]

    ### api_name1とapi_name2の類似度
    def sim_word1_word2(self, api_name1: str = "google_maps", api_name2: str = "yahoo_maps"):
        return self.model.similarity(api_name1, api_name2)

    def cbow_test(self):
        return self.model.predict_output_word(["google_maps"])
    
    def skip_test(self):
        return self.model.wv.most_similar(["google_maps"])


        
if __name__=='__main__':
    #file_name = "embeddings_4_30_200_01_06_test"
    file_name = "new_original_walks_test"
    api_name1 = "google_maps"
    api_name2 = "yahoo_maps"

    cln = Col_Node2vec(file_name)
    test = cln.node2vec(api_name1)
    test = cln.show_vector(api_name1)
    test = cln.sim_word1_word2(api_name1, api_name2)
    print(test)
    exit()
    test = cln.skip_test()
    print(test)
    test = cln.cbow_test()
    print(test)
    