# WRITING THE LOG
import pandas as pd
file_format = ['csv', 'avro', 'parquet', 'orc']
schemas = ['st','vt', 'pt']
partition = ['horizontal','predicate', 'subject']

idx = []
li=[]
# READ LOG - STORAGE FORMAT
for i in schemas:
    for j in partition:
        for k in file_format:
            # check folder
            print(f'./logs/{k}/100M_{i}_{j}.txt')

            df = pd.read_csv(f'./logs/{k}/100M_{i}_{j}.txt',sep = ',', header = None)
            df = df.fillna(0)
            avg = df.mean(axis = 0)
            li.append(avg)
            idx.append(k + f"_{i}_{j}")

# create dataframe
df = pd.DataFrame(li, index = [idx])
df = df.set_axis(["Q"+str(i+1) for i in range(11)], axis = 1)
# split dataframe
dict = {}
count = 0
loop = len(file_format)
dfs = []
for i in range(int(len(partition) * len(file_format) * len(schemas) / len(file_format))):
    dict['df_{}'.format(i)] = df[count:loop]
    count = loop
    loop = loop+4
    dfs.append(dict[f'df_{i}'])
#######################################################################################
# CREATE RANK OCCURENCES
import scipy.stats as ss
import numpy as np

rank_dataframe = []

for x in dfs:
    df_ranks = x.T
    column_names = df_ranks.columns.to_numpy().tolist()
    
    df_ranks_occurences = []
    for index, row in df_ranks.iterrows():
        df_ranks_occurences.append(ss.rankdata(row))

    df_ranks_occurences = pd.DataFrame(df_ranks_occurences)

    df_transpose = df_ranks_occurences.transpose()

    rank_table = []
    for index, row in df_transpose.iterrows():
        result_row = np.zeros(len(df_transpose.index))
        for i in range(len(row)):
            result_row[int(row[i])-1] +=1
        rank_table.append(result_row)

    rank_table = pd.DataFrame(rank_table)
    rank_table = rank_table.set_axis(column_names, axis = 'index')
    rank_table = rank_table.set_axis([i+1 for i in range(len(column_names))], axis='columns')
    rank_dataframe.append(rank_table)
#######################################################################################
# CREATE EXCEL
excel_table = dfs+rank_dataframe
xlwriter = pd.ExcelWriter('~/Desktop/rank_table.xlsx', engine='xlsxwriter')
row = 0
for dataframe in excel_table:
        dataframe.to_excel(xlwriter, sheet_name = 'storage_format_100M', startrow = row, startcol = 0)
        row = row + len(dataframe.index) + 2 
xlwriter.save()