# from PAPyA.Rank import SDRank
from PAPyA.Ranker import *
# sys.path.append("..")
# from PAPyA.Methods import FileReader

config = "D:\coding\RDF_BenchRankingLib\settings.yaml"
logs = "D:\coding\RDF_BenchRankingLib\log"
conformance_set = ['schemas', 'partition', 'storage', 'paretoAgg', 'paretoQ']
load = Coherence(config, logs,conformance_set, '100M', '250M')
print(load.run())
# FileReader(config, logs, '100M', 'schemas').file_reader()
# # df = load.file_reader()
# print(load.file_reader()) 