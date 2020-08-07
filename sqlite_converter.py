from dbfread import DBF
from re import sub
import sqlite3


def handle_db():
    db = sqlite3.connect('test.sqlite')
    cursor = db.cursor()

    try:

        cursor.execute("""CREATE TABLE IF NOT EXISTS Clienti (
                                        IdCliente integer PRIMARY KEY,
                                        Nome text NOT NULL,
                                        Cellulare text
                                    );""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Libri (
                                                    IdLibro integer PRIMARY KEY,
                                                    Titolo text NOT NULL
                                                );""")

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

    return db, cursor


def convert_customers(path, cursor):
    table_dbf = DBF(f'{path}\\CLIENTI.DBF', load=True)
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

        cursor.execute("""INSERT INTO Clienti VALUES (?,?,?)
        ON CONFLICT(IdCliente) DO UPDATE SET 
        Nome=?, Cellulare=?""", (customer['ID'], customer['NOME'], customer['CELLULARE'], customer['NOME'], customer['CELLULARE']))


def convert_books(path, cursor):
    table_dbf = DBF(f'{path}\\LIBRI.DBF', load=True)
    columns = ['ID', 'TITOLO']

    fields = table_dbf.field_names
    positions = {}

    for column in columns:
        positions[column] = fields.index(column)

    for record in table_dbf:
        book = {}

        for key, val in positions.items():
            book[key] = list(record.items())[val][1]

        cursor.execute("""INSERT INTO Libri VALUES (?,?)
            ON CONFLICT(IdLibro) DO UPDATE SET 
            Titolo=?""", (book['ID'], book['TITOLO'], book['TITOLO']))


def convert_orders(path, cursor):
    table_dbf = DBF(f'{path}\\ORDINI.DBF', load=True)
    columns = ['LIBRO', 'CLIENTE', 'DATAORD', 'ORAORD', 'FLAG']

    fields = table_dbf.field_names
    positions = {}

    for column in columns:
        positions[column] = fields.index(column)

    for record in table_dbf:
        orders = {}

        for key, val in positions.items():
            orders[key] = list(record.items())[val][1]

        cursor.execute("""INSERT INTO Ordini VALUES (?,?,?,?,?,0)
                ON CONFLICT(LibroId, ClienteId, DataOrdine, OraOrdine) DO UPDATE SET 
                Stato=?""", (orders['LIBRO'], orders['CLIENTE'], orders['DATAORD'], orders['ORAORD'], orders['FLAG'], orders['FLAG']))


def convert_to_sql(path):
    db, cursor = handle_db()
    print("Sincronizzazione Clienti...\t", end='')
    convert_customers(path, cursor)
    print("Fatto")
    print("Sincronizzazione Libri...\t", end='')
    convert_books(path, cursor)
    print("Fatto")
    print("Sincronizzazione Ordini...\t", end='')
    convert_orders(path, cursor)
    print("Fatto")
    db.commit()
    db.close()
