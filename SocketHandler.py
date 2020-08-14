import socket
import sys
import json


class SocketHandler:

    def __init__(self):
        HOST = socket.gethostname()
        PORT = 5000
        print(f"\nIndirizzo = {HOST}\nPorta = {PORT}\n\n")

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind socket to Host and Port
        try:
            soc.bind((HOST, PORT))
        except socket.error as err:
            print('Bind Failed, Error Code: ' + str(err[0]) + ', Message: ' + err[1])
            sys.exit()

        self.__soc = soc

    def start(self, data):

        self.__soc.listen(5)
        data_json = json.dumps(data)

        print(f"Rilevati {len(data)} messaggi da inviare, vuoi procedere? S/N")

        while (user_input := input().lower()) not in ['s', 'n']:
            print("Comando non riconosciuto, inserire 'S' o 'N'")

        if user_input == 'n':
            print("Operazione interrotta")
            return False

        return True
        # while 1:
        #     try:
        #         print("In attesa di connessione del telefono...")
        #         conn, addr = self.__soc.accept()
        #         print('Connesso a ' + addr[0] + ':' + str(addr[1]))
        #         conn.send(bytes(data_json + "\n", "utf-8"))
        #         conn.close()
        #         return True
        #     except Exception as e:
        #         print(f"Errore inaspettato:\n{e}")
        #         return False
