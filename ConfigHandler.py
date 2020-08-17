import json
import os
import tkinter as tk
from tkinter import filedialog


class ConfigHandler:
    __CONFIG_FILE = "config.json"
    __PATH = "path"
    __LIMIT = "limit"

    def __init__(self):

        if os.path.isfile(self.__CONFIG_FILE) and os.access(self.__CONFIG_FILE, os.R_OK):
            config_file = open(self.__CONFIG_FILE, "r")

        try:
            self.__json = json.load(config_file)
        except Exception as e:
            config_file = open(self.__CONFIG_FILE, "w")
            print("Creazione file di configurazione...")
            data = {self.__LIMIT: 180}
            root = tk.Tk()
            root.withdraw()

            directory_path = ""
            while not os.path.isfile(f"{directory_path}") or 'CLIENTI.DBF' not in directory_path:
                print("Selezionare aprire il file 'CLIENTI.DBF' di Mr.Book")
                directory_path = filedialog.askopenfilename()
                print(directory_path)
                if directory_path == "":
                    print("Operazione annullata")
                    raise FileNotFoundError

            directory_path = directory_path.replace('/CLIENTI.DBF', '')
            print(directory_path)
            data[self.__PATH] = directory_path
            json.dump(data, config_file)
            config_file.flush()
            config_file.close()
            config_file = open(self.__CONFIG_FILE, "r")
            self.__json = json.load(config_file)
            print("File di configurazione creato")

        try:
            self.path = self.__json[self.__PATH]
            self.limit = self.__json[self.__LIMIT]
        except Exception as e:
            print(e)
        config_file.close()

    def __update_value(self, new_value, key):
        self.__json[key] = new_value

        config_file = open(self.__CONFIG_FILE, "w")
        json.dump(self.__json, config_file)
        config_file.close()

    def update_path(self, new_path):
        self.__update_value(new_path, self.__PATH)

    def update_limit(self, new_limit):
        self.__update_value(new_limit, self.__LIMIT)

    def get_path(self):
        return self.path
