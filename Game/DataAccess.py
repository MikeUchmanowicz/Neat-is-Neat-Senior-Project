import mysql.connector
from mysql.connector import errorcode

import GameModels as models
    
class AIDAO():
    
    def deleteAllGen():
        try:
            connection = mysql.connector.connect(host='database-neatisneat.c030eerfzyc1.us-east-1.rds.amazonaws.com',
                                                database='neatisneat',    #CONNECT
                                                user='admin',
                                                password='password')
            if connection.is_connected():
                db_Info = connection.get_server_info()
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("Connected to MySQL Server version ", db_Info +", database: ", record)
                
                mycursor = connection.cursor()
                
                sql = "DELETE FROM Demo_datamodel"
                
                affected = mycursor.execute(sql)
                connection.commit()
                
                return affected

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
    
    def insertOneGen(data:models.DataModel):
        try:
            connection = mysql.connector.connect(host='database-neatisneat.c030eerfzyc1.us-east-1.rds.amazonaws.com',
                                                database='neatisneat',    #CONNECT
                                                user='admin',
                                                password='password')
            if connection.is_connected():
                db_Info = connection.get_server_info()
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("Connected to MySQL Server version ", db_Info +" database: ", record)
                
                mycursor = connection.cursor()
                
                sql = "INSERT INTO Demo_datamodel (gen, popsize, avgfit, stddevfit, bestfit, adjfit, stag) VALUES (%s, %s, %s,%s,%s,%s,%s)"
                val = (data.gen, data.popSize, data.avgFit, data.stdDevFit, data.bestFit, data.adjFit, data.stag)

                affected = mycursor.execute(sql, val)
                connection.commit()

                return affected

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")