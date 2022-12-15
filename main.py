import sqlite3
import datetime
import matplotlib.pyplot as plt
conn = sqlite3.connect('test.sqlite')
main_input = input('Введите вашу команду, список всех доступных команд для работы с базой данных можно узнать по команде /help')
commands = {'/demo':'Вывод 5 первых строк',
            '/show': 'Вывод несколько строк',
            '/dell': 'Удалить строку',
            '/add': 'Добавить строку',
            '/redact': 'Редактировать строку',
            '/datagraph': 'Диаграмма имеющейся суммы долга во времени',
            '/countrygraph': 'График изменения долга для имеющейся в базе страны',
            '/idgraph': 'График изменения имеющегося долга для имеющегося в базе id человека',
            '/stop': 'Закрыть программу'}
class Table():
    def __init__(self,name_table):
        self.name_table = name_table
    def get(self, start_row, last_rows):
        cursor = conn.execute(f"SELECT * FROM {self.name_table}")
        record_name_row = cursor.fetchone()
        print('{:^10}{:^10}{:^24}{:^45}{:^30}{:^24}{:^24}{:^20}{:^7}'.format(record_name_row[0],record_name_row[1],record_name_row[2],record_name_row[3],record_name_row[4],record_name_row[5],record_name_row[6],record_name_row[7],record_name_row[8]))
        records = cursor.fetchmany(last_rows)
        for row in records[start_row-1:]:
            print('{:^10}{:^10}{:^24}{:^45}{:^30}{:^24}{:^24}{:^20}{:^7}'.format(f'{row[0]}',f'{row[1]}',f'{row[2]}',f'{row[3]}',f'{row[4]}',f'{row[5]}',f'{row[6]}',f'{row[7]}',f'{row[8]}'))
    def get_column(self,number_column):
        cursor = conn.execute(f"SELECT field{number_column} FROM {self.name_table}")
        records = cursor.fetchall()
        column = []
        for row in records[1:]:
            column.append(row[0])
        return column
    def delete(self,del_row):
        conn.execute(f"DELETE from {self.name_table} where field1 = {del_row}")
        conn.commit()
        return del_row
    def add(self,id,customer_id,home,city,country,total,postalcode=None,state=None):
        conn.execute(f"INSERT INTO {self.name_table} (field1,field2,field3,field4,field5,field6,field7,field8,field9) VALUES (?,?,?,?,?,?,?,?,?)", (id, customer_id, datetime.datetime.utcnow() + datetime.timedelta(hours=3), home,city,state,country,postalcode,total))
        conn.commit()
        return id
    def redacted(self,redacted_row_id,stolb_number,new_value):
        conn.execute(
            f"UPDATE {self.name_table} SET field{stolb_number} = '{new_value}' WHERE field1 = {redacted_row_id}")
        conn.commit()
        return redacted_row_id
table = Table('invoices')
while True:
    if main_input == '/help':
        for command,specification in commands.items():
            print(command,':',specification)
    elif main_input == '/demo':
        print('Вы ввели команду /demo, держите первые 5 строк вашей базы данных','\n')
        table.get(start_row=1,last_rows=5)
    elif main_input == '/show':
        print('Вы ввели команду /show, позволяющую получить несколько строк вашей базы данных','\n')
        start_rows = int(input('Введите номер первой строки'))
        if start_rows == 0:
            start_rows =1
        last_rows = int(input('Введите номер последней строки'))
        table.get(start_rows,last_rows)
    elif main_input == '/dell':
        print('Вы ввели команду /dell, позволяющую удалить строку в вашей базе данных','\n')
        del_row = int(input('Введите номер строки которую хотите удалить'))
        print('Вы удалили строку с номером: ',table.delete(del_row))
    elif main_input == '/add':
        print('Вы ввели команду /add, позволяющую добавить строку в вашу базу данных','\n')
        column = table.get_column(1)
        id = len(column)+1
        print('Номер id для вашей новой строки: ',id)
        customer_id = int(input('Введите идентификатор пользователя'))
        home = input('Введите адрес дома')
        city = input('Введите город')
        state = input('Введите штат, если есть')
        if state == ' ' or state == '':
            state = None
        country = input('Введите страну')
        postalcode = input('Введите почтовый индекс, если есть')
        if postalcode == ' ' or postalcode == '':
            postalcode = None
        total = float(input('Введите сумму'))
        print('Строка с номером: ',table.add(id, customer_id, home, city, country, total, postalcode, state),' добавлена в базу данных')
    elif main_input == '/redact':
        print('Вы ввели команду /redact, позволяющую отредактировать строку в вашей базе данных','\n')
        redacted_row_id = int(input('Введите id строки'))
        stolb_number = int(input('Введите номер столба'))
        new_value = input('Введите значение на которое хотите изменить')
        print('Строка с номером: ',table.redacted(redacted_row_id,stolb_number,new_value),' отредактирована')
    elif main_input == '/datagraph':
        data = table.get_column(3)
        data_correction = []
        for one_data in data:
            data_correction.append(one_data[0:10])
        totals = table.get_column(9)
        totals_correction = []
        for one_total in totals:
            totals_correction.append(float(one_total))
        plt.bar(data_correction,totals_correction)
        plt.show()
    elif main_input == '/countrygraph':
        print('Вы ввели команду для вывода графика изменения долга, имеющейся в базе, страны','\n')
        countries = table.get_column(7)
        data = table.get_column(3)
        totals = table.get_column(9)
        countries_set = set(countries)
        countries_spisok = list(countries_set)
        print('Список доступных стран:', end=' ')
        for country_current in countries_spisok:
            if country_current != countries_spisok[-1]:
                print(country_current, end=', ')
            else:
                print(f'{country_current}.')
        country_input = input('Введите страну для которой хотите увидеть график долга')
        datas_one = []
        totals_one = []
        if country_input in countries_set:
            for i in range(len(countries)):
                if countries[i] == country_input:
                    datas_one.append(data[i])
                    totals_one.append(float(totals[i]))
            data_correction = []
            for data_current in datas_one:
                data_correction.append(data_current[0:10])
            plt.plot(data_correction, totals_one)
            plt.title(country_input)
            plt.show()
        else:
            print('Такой страны нет в базе')
    elif main_input == '/idgraph':
        print('Вы ввели команду для вывода графика изменения долга, имеющегося в базе, id', '\n')
        ids = table.get_column(2)
        data = table.get_column(3)
        totals = table.get_column(9)
        ids_set = set(ids)
        ids_spisok= list(map(int,ids_set))
        ids_spisok.sort()
        print('Список доступных id людей:', end=' ')
        for id_current in ids_spisok:
            if id_current != ids_spisok[-1]:
                print(id_current, end=', ')
            else:
                print(f'{id_current}.')
        id_input = input('Введите id человека для которого хотите увидеть график долга')
        datas_one = []
        totals_one = []
        if id_input in ids_set:
            for i in range(len(ids)): # для i от 0 до длины name
                if int(ids[i]) == int(id_input):
                    datas_one.append(data[i])
                    totals_one.append(float(totals[i]))
            data_correction = []
            for data_current in datas_one:
                data_correction.append(data_current[0:10])
            plt.plot(data_correction, totals_one)
            plt.title(f'Человек с id: {id_input}')
            plt.show()
        else:
            print('Такой страны нет в базе')
    elif main_input == '/stop':
        exit()
    else:
        print('Такой команды не существует, введите /help для получения доступных команд')
    main_input = input('Введите вашу команду')


