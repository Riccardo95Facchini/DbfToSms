from ipaddress import IPv4Address  # for your IP address
from pyairmore.request import AirmoreSession  # to create an AirmoreSession
from pyairmore.services.messaging import MessagingService  # to send messages
from time import sleep

class SmsSender:

    def __init__(self, ip, port):
        try:
            self.__session = AirmoreSession(IPv4Address(ip), port)
            self.__service = MessagingService(self.__session)

            accepted = self.__session.request_authorization()

            if not accepted:
                raise Exception(f'Autorizzazione non accettata')

        except Exception as e:
            print(f'Error: {e}')

    def send(self, receiver, content):
        try:
            self.__service.send_message(receiver, content)
        except Exception as e:
            print(f'Error: {e}')

    def send_all(self, rows):

        counter = 1
        sleep_each = 10
        sleep_second = 5

        for row in rows:

            if counter % sleep_each == 0:
                print("sleep")
                sleep(sleep_second)

            data = dict(row)
            # self.send(data['Cellulare'], f"Sono disponibili {data['Pronti']} libri su {data['Totale']}")
            self.send('3356760194', f"Sono disponibili {data['Pronti']} libri su {data['Totale']}")
            counter += 1

        print("FINITO")

    def close(self):
        self.__session.close()
