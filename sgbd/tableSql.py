class tableSql:
    name =""
    size = 0
    joins = {}
    fields = {}
    fieldsIdx = {}
    hashTable = {} #ver com o professor se a hash pode ficar em memoria
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
    
        
    
        