from dbfread import DBF
from re import sub
import sqlite3


class SqlHandler:
    BASE_GET_QUERY = """SELECT o.ClienteId, c.Cellulare, count(1) AS Pronti, 
                                                (Select count(1) From Ordini osub WHERE osub.Stato <> 5 AND osub.ClienteId == o.ClienteId) 
                                                AS Totale
                                                FROM Ordini o 
                                                INNER JOIN Clienti c ON c.ClienteId == o.ClienteId
                                                WHERE o.Inviato == 0 AND c.Cellulare IS NOT NULL AND (o.Stato == 2 OR o.Stato == 3) 
                                                Group BY o.ClienteId"""

    def __init__(self, path):
        self.__path = path
        db = sqlite3.connect('database.sqlite')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        try:

            cursor.execute("""CREATE TABLE IF NOT EXISTS Clienti (
                                                    ClienteId integer PRIMARY KEY,
                                                    Nome text NOT NULL,
                                                    Cellulare text
                                                );""")

            # cursor.execute("""CREATE TABLE IF NOT EXISTS Libri (
            #                                                     LibroId integer PRIMARY KEY,
            #                                                     Titolo text NOT NULL
            #                                                 );""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS Ordini (
                                                                LibroId integer NOT NULL,
                                                                ClienteId integer NOT NULL,
                                                                DataOrdine date NOT NULL,
                                                                OraOrdine date NOT NULL,
                                                                Stato integer NOT NULL,
                                                                Inviato integer,
                                                                PRIMARY KEY (LibroId, ClienteId, DataOrdine, OraOrdine)
                                                            );""")
        except Exception as e:
            print(e)

        db.commit()

        self.__db = db
        self.__cursor = cursor

    def __convert_customers(self):
        table_dbf = DBF(f'{self.__path}\\CLIENTI.DBF', load=True)
        columns = ['ID', 'NOME', 'CELLULARE']

        fields = table_dbf.field_names
        positions = {}

        for column in columns:
            positions[column] = fields.index(column)

        for record in table_dbf:
            customer = {}

            for key, val in positions.items():
                customer[key] = list(record.items())[val][1]
            customer['CELLULARE'] = sub('[^0-9]', '', customer['CELLULARE']).strip() if len(customer['CELLULARE']) else None

            self.__cursor.execute("""INSERT INTO Clienti VALUES (?,?,?)
            ON CONFLICT(ClienteId) DO UPDATE SET 
            Nome=?, Cellulare=?""", (customer['ID'], customer['NOME'], customer['CELLULARE'], customer['NOME'], customer['CELLULARE']))

    def __convert_books(self):
        table_dbf = DBF(f'{self.__path}\\LIBRI.DBF', load=True)
        columns = ['ID', 'TITOLO']

        fields = table_dbf.field_names
        positions = {}

        for column in columns:
            positions[column] = fields.index(column)

        for record in table_dbf:
            book = {}

            for key, val in positions.items():
                book[key] = list(record.items())[val][1]

            self.__cursor.execute("""INSERT INTO Libri VALUES (?,?)
                ON CONFLICT(LibroId) DO UPDATE SET 
                Titolo=?""", (book['ID'], book['TITOLO'], book['TITOLO']))

    def __convert_orders(self):
        table_dbf = DBF(f'{self.__path}\\ORDINI.DBF', load=True)
        columns = ['LIBRO', 'CLIENTE', 'DATAORD', 'ORAORD', 'FLAG']

        fields = table_dbf.field_names
        positions = {}

        for column in columns:
            positions[column] = fields.index(column)

        for record in table_dbf:
            orders = {}

            for key, val in positions.items():
                orders[key] = list(record.items())[val][1]

            self.__cursor.execute("""INSERT INTO Ordini VALUES (?,?,?,?,?,0)
                    ON CONFLICT(LibroId, ClienteId, DataOrdine, OraOrdine) DO UPDATE SET 
                    Stato=?""", (orders['LIBRO'], orders['CLIENTE'], orders['DATAORD'], orders['ORAORD'], orders['FLAG'], orders['FLAG']))

    def convert(self):
        print("Inizio sincronizzazione:\n")
        print("Sincronizzazione Clienti...\t", end='')
        self.__convert_customers()
        print("Fatto")
        # print("Sincronizzazione Libri...\t", end='')
        # self.__convert_books()
        # print("Fatto")
        print("Sincronizzazione Ordini...\t", end='')
        self.__convert_orders()
        print("Fatto")
        self.__db.commit()

    def set_sent(self, user_list):

        for user_id in user_list:
            self.__cursor.execute("""UPDATE Ordini SET Inviato = 1 WHERE Stato IN (2,3) AND ClienteId == ?""", (user_id,))

        self.__db.commit()

    def __get_all_ready_query(self, limit):

        query_body = self.BASE_GET_QUERY + f""" HAVING Pronti == Totale"""

        if limit:
            query_body += f""" LIMIT {limit}"""

        return query_body

    def __get_partial_ready_query(self, limit):
        query_body = self.BASE_GET_QUERY + f""" HAVING Pronti <> Totale"""

        if limit:
            query_body += f""" LIMIT {limit}"""

        return query_body

    def get_to_send(self, limit=None):

        query_body = self.__get_all_ready_query(limit)

        query = self.__cursor.execute(query_body)
        rows = query.fetchall()

        print(f"Prima estrazione = {len(rows)}")

        if len(rows) < limit:
            query_body = self.__get_partial_ready_query(limit - len(rows))
            query = self.__cursor.execute(query_body)
            rows.extend(query.fetchall())
            print(f"Seconda estrazione = {len(rows)}")

        print(f"Messaggi da inviare = {len(rows)}")

        result = list(map(dict, rows))  # Maps sqlite rows to list of dictionaries
        return result

    def close(self):
        self.__db.close()
