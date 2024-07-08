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
        sql_check_id = """
                        SELECT id  FROM Users WHERE ID_EXT = ?
                    """
        sql_check_name = """
                                SELECT id  FROM Users WHERE name = ?
                            """

        # Проверка наличия игрока

        flag1 = cursor.execute(sql_check_id,id_ext).fetchone()
        flag2 = cursor.execute(sql_check_name,name).fetchone()

        if flag1 or flag2:
            return 'Имя/ID уже присутствует в БД!'

        cursor.execute(sql,(id_ext,name))
        cursor.commit()
        cursor.close()
        return False


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
        sql_check = """
                        SELECT id FROM message_logs WHERE  date_str = ? and id_ext = ?
                    """
        flag = cursor.execute(sql_check,(date_str, message['id'])).fetchone()
        if not flag:
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
            INNER JOIN Users ON message_logs.id_ext = Users.ID_EXT WHERE message_logs.date_str = ? AND message_logs.approve = 0
        """
        res = cursor.execute(sql_select, date_str).fetchall()
        cursor.close()
        return res

    def check_admin_user(self,id_ext:int):
        cursor = self.conn.cursor()

        sql = """
                              SELECT is_admin FROM Users  WHERE ID_EXT = ?
                             """

        temp_res = cursor.execute(sql,id_ext)
        res = temp_res.fetchone()
        if res:
            return res[0]
        else:
            return False



data = Data('./Calendar.mdb')


