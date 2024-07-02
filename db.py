import pyodbc


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


    def delete_player(self,id_ext,name:str):
        cursor = self.conn.cursor()

        sql = """
                DELETE FROM Users Where ID_EXT = ?
              """

        cursor.execute(sql,(id_ext,name))
        cursor.commit()
        cursor.close()
        return True








data = Data('./Calendar.mdb')

