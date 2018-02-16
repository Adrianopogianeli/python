import MySQLdb

class clsDB(object):

    _servidor="127.0.0.1"
    _banco = "oracle"
    _usuario = "root"
    _senha="121212"
    _cnn=None
    _socket="/home/mysql/mysql.sock"
    
    def executaQuery(self,sHost=None,user_db=None,mkdt=None,sDb=None,sQuery=None):
        try:
            if sHost == None:
                sHost=self._servidor
            if user_db == None:
                user_db = self._usuario
            if mkdt == None:
                mkdt = self._senha
            if sDb == None:
                sDb = self._banco
            if "localhost" in sHost or "127.0.0.1" in sHost:
                conn = MySQLdb.connect(
                host=sHost,
                db=sDb,
                user=user_db,
                passwd=mkdt
                #,unix_socket=self._socket
                )
            else:
                conn = MySQLdb.connect(
                host=sHost,
                db=sDb,
                user=user_db,
                passwd=mkdt
                )
            cur = conn.cursor()
            cur.execute(sQuery)
            retorno = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            retorno = "Erro no metodo executaQuery: %s"%e
            conn.rollback()
            cur.close()
            conn.close()
        finally:
            return retorno

        
if __name__ == '__main__':
    teste = clsDB()
    print teste.executaQuery(None,None,None,None,"show databases")
    pass



