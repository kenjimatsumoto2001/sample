"""
f = open("./csv_sample/embeddings_4_30_200_01_06_sg01_No1.csv","r")
g = open("./csv_sample/embeddings_4_30_200_01_06_sg01_No1_num.csv","a")
lines  = f.readlines()[1:]
for i in lines:
	i = i.split(",")
	num = 0
	line_num = len(i)
	for j in range(line_num):
		if num == 0:
			num += 1
			pass
		elif num == line_num -1:
			n = i[j]
			g.write(str(n))
		else:
			n = i[j]
			n = n.replace('\n','')
			g.write(str(n) + ",")
			num += 1
"""
class Sakujo:
	def del_gyou_retu(self, input_file, output_file):
		f = open(input_file, "r")
		g = open(output_file, "a")
		lines  = f.readlines()[1:]
		for i in lines:
			i = i.split(",")
			num = 0
			line_num = len(i)
			for j in range(line_num):
				if num == 0:
					num += 1
					pass
				elif num == line_num -1:
					n = i[j]
					g.write(str(n))
				else:
					n = i[j]
					n = n.replace('\n','')
					g.write(str(n) + ",")
					num += 1

if __name__=='__main__':
	sk = Sakujo()
	sk.del_gyou_retu("original_walks_128_30_50_late.csv", "original_walks_128_30_50_late_num.csv")