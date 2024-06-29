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

data = Data('./Calendar.mdb')