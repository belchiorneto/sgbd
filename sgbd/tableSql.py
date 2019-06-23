import os.path
from os import path

class tableSql:
    name =""
    size = 0
    joins = {}
    fields = {}
    fieldsIdx = {}
    hashTable = {} #ver com o professor se a hash pode ficar em memoria
    buffer = {}
    bufferlimit = 500000; #~ 2MB de buffer 
    def __init__(self,nome, joins, fields, size, fieldidx):
        self.name = nome
        self.joins = joins
        self.fields = fields
        self.size = size
        self.fieldsIdx = fieldidx
    
    def sethashTable(self, hashtable):
        self.hashTable = hashtable
    
    # necessario para o .sort()
    def __lt__(self, other):
        return self.size < other.size
    
    def getBufferSize(self):
        retorno = 0;
        for k in self.buffer:
            retorno += len(self.buffer[k])
        return retorno
    
    def descarregarBucket(self):
        for hashkey in self.buffer:
            nomearq = "Bucket" + str(hashkey) + ".txt"
            if path.exists(self.name+"/"+nomearq):
                nomearq = nomearq
            else:
                arq_bucket = open(self.name+"/"+nomearq, "a").close()
            bucket = open(self.name+"/"+nomearq, "a+")
            bucket.write(self.buffer[hashkey])
            self.buffer[hashkey] = ""
            bucket.close()
    def descarregarDados(self):
        for hashkey in self.buffer:
            nomearq = self.name+ ".txt"
            if path.exists(self.name+"/"+nomearq):
                nomearq = nomearq
            else:
                arq_bucket = open(self.name+"/"+nomearq, "a").close()
            file = open(self.name+"/"+nomearq, "a+")
            file.write(self.buffer[hashkey])
           
            self.buffer[hashkey] = ""
            file.close()
    
        
    
        