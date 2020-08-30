from sql_handler import SqlHandler
from socket_handler import SocketHandler
from config_handler import ConfigHandler


def message_maker(sql_data):
    format_data = []
    for row in sql_data:
        format_data.append({"Cellulare": row["Cellulare"],
                            "Messaggio": f"Cartoleria San Lazzaro: messaggio automatico non rispondere\nGentile cliente sono disponibili n.{row['NewPronti'] + row['OldPronti']} libri/fascicoli. Mancano ancora n.{row['Rimanenti']} libri/fascicoli"})
    return format_data


config = None

try:
    config = ConfigHandler()
except FileNotFoundError:
    print("Deve essere specificato il file 'CLIENTI.DBF'.\nPremere qualsiasi tasto per chiudere...")
    input()
    exit(1)

socket = SocketHandler()
sql_handler = SqlHandler(config.path)
sql_handler.convert()
sql_data = sql_handler.get_to_send(config.limit)

if len(sql_data) == 0:
    print("Nessun nuovo ordine da comunicare.\nPremere qualsiasi tasto per chiudere...")
    input()
    exit(1)

data = message_maker(sql_data)
# data = sql_handler.get_test_data("", 5)

print(data)

sent = socket.start(data)
if sent:
    users = list(map(lambda d: str(d['Cellulare']), sql_data))
    sql_handler.set_sent(users)
    sql_handler.close()
    print("Messaggi inviati")

input()
