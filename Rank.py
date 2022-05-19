from abc import ABC, abstractmethod

class Rank(ABC):
    @abstractmethod
    #new method that works for ranking in sd and md
    def calculateRankScore(self):
        pass 
    @abstractmethod
    def loader(self):
        pass
    @abstractmethod
    def file_reader(self):
        pass
    @abstractmethod
    def plot(self):
        pass