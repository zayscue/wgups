import abc

class HashTable(abc.ABC):
    @abc.abstractmethod
    def insert(self, item):
        pass
    
    @abc.abstractmethod
    def search(self, key):
        pass

    @abc.abstractmethod
    def remove(self, key):
        pass