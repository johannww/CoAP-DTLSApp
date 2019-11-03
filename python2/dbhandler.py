#!/usr/bin/env python 1
# -*- coding: utf-8 -*-

import sys
#import MySQLdb
       
class DataBase(object):
    """docstring for ClassName"""
    def __init__(self):
        self.cursor = None;
        self.db = None;
        
    def connect_db(self):
        try:
            self.db = MySQLdb.connect("localhost","dtlsapp","johann","IoT")
            self.cursor = self.db.cursor()
        except:
            print("Não se pode conectar ao servidor de banco de dados")
            print("TERMINANDO...")
            #sys.exit()

    def on_message(self, dados):
        lista = dados.split("/") ############# EXEMPLO QUE DEVE SER ENVIADO DA RASPBERRY >>>> "5C:CF:7F:53:BA:34/25.4/1.0/-27.60044, -48.51884"
                                                                                              #        SENSOR            MAC_SENSOR         TEMP         FLUXO             GPS				TEMPO    
        sql = 'INSERT INTO IoT.dados(sensor,mac_sensor,temp,fluxo_agua,gps,data_ins) VALUES ("'+ lista[0]+'","'+lista[1]+'", '+lista[2]+', '+lista[3]+',"'+str(lista[4])+'", CURRENT_TIMESTAMP);'
        try:  
            self.cursor.execute(sql)
            self.db.commit()
        except:
            #self.db.rollback()
            print("Falha ao gravar no Banco de Dados!")

