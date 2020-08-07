from dbfread import DBF
from tabulate import tabulate


def print_table(path, amount):
    table = DBF(path, load=True)

    if amount <= 0:
        amount = len(table.records)

    fields = table.field_names

    for i in range(amount):
        record = table.records[i].values()
        for val in zip(fields, record):
            print(val)


def print_table_column(path, column, amount=0):
    table = DBF(path, load=True)

    if amount <= 0:
        amount = len(table.records)

    fields = table.field_names
    position = fields.index(column)

    for i in range(amount):
        record = list(table.records[i].items())
        print(record[position])


def print_table_columns(path, columns, amount=0):
    table = DBF(path, load=True)

    if amount <= 0:
        amount = len(table.records)

    fields = table.field_names

    positions = []

    for column in columns:
        positions.append(fields.index(column))

    for rec in table:
        print(type(rec))
        print(rec)
        j = 0
        for i in positions:
            print(list(rec.items())[i][1])
            j += 1
        break

    # print_table = []
    # for i in range(amount):
    #     record = list(table.records[i].items())
    #     row = []
    #     for position in positions:
    #         row.append(str(record[position][1]))
    #     print_table.append(row)
    # print(tabulate(print_table, headers=columns, tablefmt="github"))
