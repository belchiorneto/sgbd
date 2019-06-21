from tableSql import *
class sqlFormat(object):
    tabelas = []
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
            print(joins)
            fields = self.getfieldsFromSqlCmd(tabs[i])
            self.tabelas.append(tableSql(tabs[i], joins, fields))
            

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
        retorno = []
        # joins
        joins = sqlcmd.split("where");
        ands = joins[1].split("and")
        if(len(ands) > 1):
            #mais de uma condição de junção
            joins = joins[1].split("and")
            
            joins[i] = joins[i].strip()
            for i in range(len(joins)):
                partes = joins[i].split(" = ")
                for parte in partes:
                    if(parte.split(".")[0] == tab):
                        retorno.append(parte.split(".")[1])
        else:
            #apenas uma condicao de juncao
            
            partes = joins[1].split(" = ")
            for parte in partes:
                if(parte.split(".")[0] == tab):
                    retorno.append(parte.split(".")[1])
        return retorno
                
        
           
                
        