import pyodbc
from factory import make_str

class Data:
    def __init__(self, road):
        self.static_road = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + road
        self.conn = pyodbc.connect(self.static_road)


    def select_player_name(self,id_ext:str):
            cursor = self.conn.cursor()

            sql = """
                   SELECT name FROM Users Where ID_EXT = ?
                  """

            temp_res = cursor.execute(sql, id_ext)
            res = temp_res.fetchone()
            if res:
                return res[0]
            else:
                return None

    def select_all_players(self):
            cursor = self.conn.cursor()

            sql = """
                   SELECT ID_EXT,name FROM Users 
                  """

            temp_res = cursor.execute(sql)
            res = temp_res.fetchall()
            cursor.close()
            return [i for i in res]

    def insert_player(self,id_ext,name:str):
        cursor = self.conn.cursor()

        sql = """
              Insert into Users (ID_EXT,name)
                       VALUES (?,?)  
              """

        cursor.execute(sql,(id_ext,name))
        cursor.commit()
        cursor.close()
        return True


    def delete_player(self,id_ext):
        cursor = self.conn.cursor()

        sql = """
                DELETE FROM Users Where ID_EXT = ?
              """

        cursor.execute(sql,id_ext)
        cursor.commit()
        cursor.close()

    def select_all_players_new(self):
        cursor = self.conn.cursor()

        sql = """
                      SELECT ID_EXT,name FROM Users 
                     """

        temp_res = cursor.execute(sql)
        res = temp_res.fetchall()
        cursor.close()
        return [{'id':i[0],'name':i[1],'event':[]} for i in res]


    def insert_message_logs(self,date_str:str,message:dict):

        cursor = self.conn.cursor()

        sql = """
                      Insert into message_logs (date_str,id_ext,message_str,approve)
                               VALUES (?,?,?,?)
                      """

        cursor.execute(sql, (date_str, message['id'],make_str(message['event']),0))
        cursor.commit()
        cursor.close()


    def change_status_message(self,date_str:str,id_ext:str):
        cursor = self.conn.cursor()

        sql_update = """
                              Update message_logs SET approve = ? WHERE date_str = ? AND id_ext = ?
                           """
        cursor.execute(sql_update, (1,date_str, id_ext))
        cursor.commit()
        cursor.close()

    def select_events_by_date(self,date_str:str):
        cursor = self.conn.cursor()
        sql_select = """
            SELECT message_logs.date_str, message_logs.id_ext, message_logs.approve, Users.name
            FROM message_logs
            INNER JOIN Users ON message_logs.id_ext = Users.ID_EXT WHERE message_logs.date_str = ?
        """
        res = cursor.execute(sql_select, date_str).fetchall()
        cursor.close()
        return res



data = Data('./Calendar.mdb')

#print(data.select_events_by_date('06.07.2024'))
