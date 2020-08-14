from SqlHandler import SqlHandler
from SocketHandler import SocketHandler

socket = SocketHandler()
sql_handler = SqlHandler(r'D:\Download\postumia')
sql_handler.convert()
data = sql_handler.get_to_send(195)

sent = socket.start(data)

if sent:
    users = list(map(lambda d: str(d['ClienteId']), data))
    sql_handler.set_sent(users)

sql_handler.close()
print("Completato")

# sender = DataSender('192.168.1.9', 2333)
# sender.send_all(to_send)
# sender.send('3356760194', 'test')
# sender.send('3356760194', 'test2')
# sender.close()
