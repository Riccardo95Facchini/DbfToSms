# Methods used only for testing purposes #

import os
import csv
from dbfread import DBF


def create_csvs(path, files=[]):
    # path = 'D:\\Download\\postumia'

    for file in os.listdir(path):
        if file.lower().endswith(".dbf"):
            table = DBF(f'{path}\\{file}', load=True)

            if len(table.records) <= 0 or (files and file not in files):
                print(f'Skipping {file}')
                continue

            print(f'Reading {file}')

            with open(f"{path}\\csvs\\{file[:file.lower().index('.dbf')]}.csv", 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(table.field_names)
                for record in table:
                    writer.writerow(list(record.values()))
                csv_file.close();
