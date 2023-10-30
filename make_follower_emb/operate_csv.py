#csvファイルの操作
#主に，各サービスごとの類似度をcsvに書き込む際に仕様する
import csv
import pandas as pd

class Op_Csv:
    def __init__(self):
        pass

    def write_csv(self, data, file_pass):
        with open(file_pass, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def load_csv(self, file_pass):
        df = pd.read_csv(file_pass)
        return df

if __name__=='__main__':
    #使い方
    import col_node2vec
    file_name = "embeddings_4_30_200_01_06_test"
    cln = col_node2vec.Col_Node2vec(file_name)
    api_name_list = ["google_maps", "yahoo_maps", "bing_maps"]
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

    #csv操作
    csv_pass = "./csv/test.csv"
    op_csv = Op_Csv()
    op_csv.write_csv(result_list, csv_pass) #csvへの書き込み
    