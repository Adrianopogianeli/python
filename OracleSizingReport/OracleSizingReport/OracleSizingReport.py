#Programa para efetuar os ajustes nos arquivos de auditoria da oracle
import fileinput
import sys
import logging
import os
import MySQLdb
from clsDB import clsDB
import re

class OracleChangeScript:

    def __init__(self):
        self._arquivo_log = "C:\\temp\\OracleChangeScript.log"
        self._string_del_linha = "remover" #identificador utilizado para deletar a linha
        self._diretorio = "C:\\temp\\scripts_oracle_fev2018\\"
        logging.basicConfig(filename=self._arquivo_log,\
            level=logging.INFO,format="%(asctime)s %(message)s",datefmt="[%d/%m/%Y %H:%M:%S]")

    def FileList(self, diretorio):
       try:
           if diretorio is None:
               diretorio = self._diretorio
           resultado = []
           for folder, subfolders, files in os.walk(diretorio):
               for file in files:
                   resultado.append(str(os.path.join(os.path.abspath(folder), file)))
       except Exception as e:
           logging.info("Erro na func FileList: %s "%e)
           print "Erro na func FileList: %s"%e
       return resultado


    def ImportMetrics(self, arquivo,dicRemove):

        row_delete = OracleChangeScript()
        if row_delete.ReplaceLine(arquivo,dicRemove) is True:
            mysql = clsDB()
            command_db = "create database oracle"
            command_table = "create table metrics(SCRIPT varchar(200),METRIC_NAME varchar(50),DBID BIGINT,INSTANCE_NUMBER INT, \
                             SNAP_ID INT,TIMEREF INT,END_TIME DATETIME,MINVAL FLOAT,  \
		    			     MAXVAL FLOAT,AVERAGE FLOAT,STANDARD_DEVIATION FLOAT)"
            
            f = open(arquivo,"r")
            novo_arquivo = f.readlines()
            f.close()
            for line in novo_arquivo:
                if len(line)>0:
                    #extracao do txt metrics por coluna
                    SCRIPT = arquivo[31:].strip() # len do path C:\\temp\\scripts_oracle_fev2018\\
                    METRIC_NAME = line[0:51].strip()
                    DBID = line[52:62] .strip()
                    INSTANCE_NUMBER = line[62:78].strip()
                    SNAP_ID = line[78:89].strip()
                    TIMEREF = line[89:102].strip()
                    END_TIME = line[102:118].strip()
                    MINVAL = line[118:129].strip()
                    MAXVAL = line[129:140].strip()
                    AVERAGE = line[140:151].strip()
                    STANDARD_DEVIATION = line[151:170].strip()
                    if METRIC_NAME != "":
                         #print SCRIPT,METRIC_NAME,DBID,INSTANCE_NUMBER,SNAP_ID,TIMEREF,END_TIME,MINVAL,MAXVAL,AVERAGE,STANDARD_DEVIATION
                         command_sql = "insert into oracle.metrics values( \
                                  '%s','%s', '%s','%s','%s','%s', \
                                  str_to_date('%s','%%d/%%m/%%Y %%H:%%i'),'%s', \
                                  '%s','%s','%s' \
                                   )"%(SCRIPT,METRIC_NAME,DBID,INSTANCE_NUMBER,SNAP_ID,\
                                      TIMEREF,END_TIME,MINVAL, \
                                      MAXVAL,AVERAGE,STANDARD_DEVIATION)
                         print command_sql
                         print mysql.executaQuery("127.0.0.1","root",None,"oracle",command_sql)
                    else:
                        print "Linhas vazias serao desconsideradas: %s"%SCRIPT,METRIC_NAME,DBID,INSTANCE_NUMBER
                        logging.info("Linhas vazias serao desconsideradas: %s %s %s %s \n"%(SCRIPT,METRIC_NAME,DBID,INSTANCE_NUMBER))
        else:
            logging.info("Erro de OracleChangeScript no arquivo %s \n"%(arquivo))
        #mysql.executaQuery("127.0.0.1","root",None,"oracle","show tables")
        #return msn
        
  

    def ReplaceLine(self,arquivo,dicReplace):
        try:
            linha = 0
            f = open(arquivo,"r")
            novo_arquivo = f.readlines()
            f.close()
            f = open(arquivo,"w")
            logging.info("Inicio do processamento do arquivo %s \n"%(arquivo))
            print "Inicio do processamento do arquivo %s \n"%(arquivo)
            for line in novo_arquivo:
                linha = linha +1
                for searchExp,replaceExp in dicReplace.iteritems():
                    if str(searchExp).strip() in str(line).strip():
                        line = replaceExp
                        print "O valor da linha %s : %s sera substituido por: %s"%(linha,searchExp,replaceExp)
                        logging.info("O valor da linha %s : %s sera substituido por: %s"%(linha,searchExp,replaceExp))   
                #removendo linhas *remover
                if str(self._string_del_linha).strip() not in str(line).strip():
                    f.write(line)
                else:
                    logging.info("A linha: %s foi removida"%line)
                    print "A linha: %s foi removida"%line                    
            f.close()
            logging.info("Fim do processamento, Total de linhas verificadas %s"%linha)
            print "Fim do processamento, Total de linhas verificadas %s"%linha
        except Exception as e:
            print "Erro na func ReplaceLine: %s"%e
            return False
        return True


        
        


if __name__ == '__main__':        
#Linhas as serem substituidas
   param_dbinfo = \
   "control_management_pack_access;control_management_pack_access                                                            1 NONE\n,\
   ADDM;remover                                                                        ,\
   awr_snapshot_time_offset;awr_snapshot_time_offset								  1 0 ,\
   AWR;remover                                                                         ,\
   EM Performance;remover                                                              ,\
   SQL Monitoring and Tuning pages;remover                                             ,\
   SQL Tuning Advisor;remover                                                          ,\
   selected.;remover                                                                \
   "
   param_metrics = \
   "inicial;remover                                                                        ,\
    final;remover                                                                        ,\
    METRICS;remover                                                                        ,\
    METRIC_NAME;remover                                                                        ,\
    ----;remover                                                                        ,\
    selected;remover                                                                        ,\
    STAT_NAME;remover                                                                        ,\
    NUM_;remover                                                                        ,\
    LOAD;remover                                                                        ,\
    TCP_;remover                                                                        ,\
    PHYSICAL_;remover                                                                        ,\
    GLOBAL_;remover                                                                        ,\
    NO;remover                                                                        \
   "
   #Convert param string to dic
   dic_dbinfo = dict((p.split(';') for p in param_dbinfo.split(',')))
   dic_metrics = dict((p.split(';') for p in param_metrics.split(',')))
   #Iniciar
   #arquivo = "C:\\temp\\scripts_oracle_fev2018\\ORAINST1_NSCFN4UCS3D1860.txt"
   #ajuste = OracleChangeScript()
   #ajuste.ReplaceLine(arquivo,dic_param)
# Leitura de todos os arquivos da pasta 
   ajuste = OracleChangeScript()
   for file in ajuste.FileList(None):
# ajuste dos scripts dbinfo
       if 'dbinfo' in file:
           print ajuste.ReplaceLine(file,dic_dbinfo)
# ajuste dos scripts metrics
       if 'metrics' in file:
           print ajuste.ImportMetrics(file,dic_metrics)








