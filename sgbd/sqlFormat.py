import os
import time
import string
import os.path
from os import path


from tableSql import *
from random import paretovariate

class sqlFormat(object):
    tabelas = []
    readOP = 0;
    writeOp = 0;
    def __init__(self,cursor, sqlcmd):
        self.cursor = cursor
        self.sql = sqlcmd
        

    def getTableFromSqlCmd(self):
        sqlcmd = self.sql.lower()
        # tabelas
        tabs = sqlcmd.split(" from ");
        if(len(tabs[1].split(" on ")) > 1):
            # caso de join
          
            tabs = tabs[1].split(" on ");
            tabs = tabs[0].split(" join ")
        else:
            # caso separado por virgula
           
            tabs = tabs[1].split(" where ")
            tabs = tabs[0].split(",")
        for i in range(len(tabs)):
            tabs[i] = tabs[i].strip()
            joins = self.getJoinFromSqlCmd(tabs[i])
            fields = self.getfieldsFromSqlCmd(tabs[i])
            fieldidx = self.getfieldIdex(tabs[i], fields)
            size = self.tableSize(tabs[i])
            
            self.tabelas.append(tableSql(tabs[i], joins, fields, size, fieldidx))
            

    def getfieldsFromSqlCmd(self, tab):
        sqlcmd = self.sql.lower()
        # campos
        fields = sqlcmd.split("from");
        fields = fields[0].split("select")
        fields = fields[1].split(",")
        retorno = []
        
        for i in range(len(fields)):
            fields[i] = fields[i].strip()
            if(fields[i].split(".")[0] == tab):
                retorno.append(fields[i].split(".")[1])
        return  retorno           
    
    
    def getJoinFromSqlCmd(self, tab):
        sqlcmd = self.sql.lower()
        retorno = {}
        # joins
        joins = sqlcmd.split("where");
        ands = joins[1].split("and")
        if(len(ands) > 1):
            #mais de uma condição de junção
            joins = joins[1].split("and")
            for i in range(len(joins)):
                joins[i] = joins[i].strip()
                if tab in joins[i]:
                    partes = joins[i].split(" = ")
                    t1 = partes[0].split(".")[0]
                    t2 = partes[1].split(".")[0]
                    c1 = partes[0].split(".")[1]
                    c2 = partes[1].split(".")[1]
                    retorno[t1+"."+t2] = c1
                    #volta t2.c2 = t1.c1
                    retorno[t2+"."+t1] = c2
                
        else:
            #apenas uma condicao de juncao
            
            partes = joins[1].split(" = ")
            for i in range(len(partes)):
                partes[i] = partes[i].strip()
            t1 = partes[0].split(".")[0]
            t2 = partes[1].split(".")[0]
            c1 = partes[0].split(".")[1]
            c2 = partes[1].split(".")[1] 
            retorno[t1+"."+t2] = c1
            retorno[t2+"."+t1] = c2
        return retorno
    
    def tableSize(self, tab):
        self.cursor.execute("select count(*) from "+ tab)
        for row in self.cursor:
            for s in row:
                return s
    
    def getfieldIdex(self, tab, campos):
        camposindex = {}
        
        self.cursor.execute("SELECT column_name from information_schema.columns where table_name = '"+tab+"'")
        i = 0
        for row in self.cursor:
            for campo2 in row:
                for campo in campos:
                    if(campo == campo2):
                        camposindex[campo] = i;
                        
                i = i + 1
        return camposindex
    
    def criaDiretorios(self):
        tabelas = self.tabelas
        count = len(tabelas)
        while (count >= 0):
            folder = "" #para as pastas com mais de uma tabela
            for i in range(count):
                
                if(i == count-1):
                    folder = folder + tabelas[i].name
                else:
                    folder = folder + tabelas[i].name + "_"
            if(count > 0):
                try:
                    os.mkdir(folder)
                except FileExistsError:
                    FileExistsError.errno
            else:
                for k in range(len(tabelas)):
                    try:
                        os.mkdir(tabelas[k].name)
                    except FileExistsError:
                        FileExistsError.errno
            count = count - 1
    def gerarTXTs(self):
        for tab in self.tabelas:
            arqtab = tab.name + ".txt"
            open(arqtab, 'w').close()
            arquivo = open(arqtab, "a+")
            inicio = time.time()
            self.cursor.execute("SELECT * from "+tab.name+"")
            
            for row in self.cursor:
                auxiliar = ""
                for campo in row:
                    auxiliar = auxiliar + str(campo) + " "
                arquivo.write(str(auxiliar) + '\n')
                
        
            fim = time.time()
            print("Tempo total para gerar txt da tabela "+tab.name+": ",fim-inicio)
    
    def geraHashTables(self):
        inicio = time.time()
        tabelas = self.tabelas
        for tab in tabelas:
            print("tabela: " + tab.name)
            arquivo = open(tab.name + ".txt", "r")
            self.readOP = self.readOP + 1; 
            hashTable = {}
            for linha_arquivo in arquivo:
                campos = linha_arquivo.split(" ")
                for key in tab.joins:
                    if key.split(".")[1] != tab.name:
                        hashkey = self.funcaoHashGeneric(campos[tab.fieldsIdx[tab.joins[key]]], tab.size)
                        hashTable[hashkey] = campos[tab.fieldsIdx[tab.joins[key]]]
            arquivo.close()
           
            tab.sethashTable(hashTable)
            fim = time.time()
            print("Tempo total para gerar hashtable em "+tab.name+": ",fim-inicio)
    def geraBuckets(self):
        inicio = time.time()
        tabelas = self.tabelas
        for tab in tabelas:
            print("tabela: " + tab.name)
            
            # criar buckets
            
            for hashkey in tab.hashTable:
                arq_bucket_criacao = self.criarBucket(hashkey, tab.name)
                buffer = ""
                bufferindex = 0;
                arquivo = open(tab.name + ".txt", "r")
                for linha_arquivo in arquivo:
                    campos = linha_arquivo.split(" ")
                    for key in tab.joins:
                        if key.split(".")[1] != tab.name:
                            newhash = self.funcaoHashGeneric(campos[tab.fieldsIdx[tab.joins[key]]], tab.size)
                            if(hashkey == newhash):
                                buffer = buffer + linha_arquivo
                                bufferindex = bufferindex + 1
                            
                print(str(len(buffer)))
                preencher_bucket = self.preencherBucket(buffer, arq_bucket_criacao, tab.name)
                arquivo.close()
            
            fim = time.time()
            print("Tempo total para gerar bucket em "+tab.name+": ",fim-inicio)
    
    def criarBucket(self, valor, tab):
        nomearq = "Bucket" + str(valor) + ".txt"
        if path.exists(tab+"/"+nomearq):
            return nomearq
        else:
            arq_bucket = open(tab+"/"+nomearq, "a").close()
            self.readOP = self.readOP + 1;
            return nomearq

    def preencherBucket(self, tuplaInteira, nomearq, tab):
        bucket = open(tab+"/"+nomearq, "a+")
        
        self.readOP = self.readOP + 1; 
        bucket.write(tuplaInteira)
        self.writeOp = self.writeOp + 1; 
        bucket.close()

    def joins(self, tabNum):
        inicio = time.time()
        tabA = self.tabelas[tabNum]
        tabB = self.tabelas[tabNum + 1]
        
        if tabA.size > tabB.size:
            tabA = self.tabelas[tabNum + 1]
            tabB = self.tabelas[tabNum]
        
        for hashValue in tabA.hashTable: 
            indice = hashValue
            bucketA = open(tabA.name+"/Bucket"+str(indice)+".txt","r")
            for key in tabA.joins:
                if key.split(".")[1] == tabA.name:
                    continue
                atriJuncaoA = tabA.fieldsIdx[tabA.joins[key]]
                
                for hashValueB in tabB.hashTable:
                    indiceB = hashValueB
                    bucketB = open(tabB.name+"/Bucket"+str(indiceB)+".txt","r")
                    atriJuncaoB = tabB.fieldsIdx[tabB.joins[tabB.name +"."+tabA.name]]
                    try:
                        os.mkdir(tabA.name+"_"+tabB.name)
                    except FileExistsError:
                        FileExistsError.errno
                    tabAB = open(tabA.name+"_"+tabB.name+"/"+tabA.name+"_"+tabB.name+".txt","a+")
                    for A in bucketA:
                        linhaA = A.split()
                        for B in bucketB:
                            linhaB = B.split()
                            if (linhaA[atriJuncaoA]==linhaB[atriJuncaoB]):
                                
                                linhafinal = ""
                                for item in linhaA:
                                    linhafinal = linhafinal + item + " "
                                for item in linhaB:
                                    linhafinal = linhafinal + item + " "
                                
                                tabAB.write(linhafinal+"\n")
                        tabAB.close()
                bucketB.close()
            bucketA.close()
        fim = time.time()
        print("Tempo total Join "+ tabA.name+ " com " +tabB.name + ": ",fim-inicio)
        
        if(tabNum < len(self.tabelas) - 2):
            # chama recursivo ate a penultima tabela
            self.joins(tabNum + 1)

    
        
    def funcaoHashGeneric(self, key, tablesize):
        value = 0
        #caso seja string
        if(isinstance(key, str)):
            for char in key:
                value = value + ord(char)
        else:
            value = key

        a = 30
        b = 45
        p = 4091
        chave_hash = ((a*value + b)% p) % tablesize
        return chave_hash
    
    def escritas(self):
        return self.writeOp
    def leituras(self):
        return self.readOP                
           
                
        