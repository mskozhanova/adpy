from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
#pprint(contacts_list)

## 1. Выполните пункты 1-3 задания.
## Ваш код

def merge(col, newcol):
    if(len(col) == 0):
        return newcol
    else:
        return col

headers = {}
for i in range(len(contacts_list[0])):
  headers[contacts_list[0][i]] = i
#pprint(headers)

tmp = {}

for i in range(1, len(contacts_list)):
    #pprint(contacts_list[i])
    myrow = contacts_list[i]

    lastname = myrow[headers['lastname']]
    firstname = myrow[headers['firstname']]
    surname = myrow[headers['surname']]

    fio = (f"{lastname} {firstname} {surname}").strip()
    fi = (f"{lastname} {firstname}").strip()

    result = re.findall(r"\w+", fio)
    #pprint(result)

    if len(result) == 3:
        if not fio in tmp:
            tmp[fio] = {
                'lastname': result[0],
                'firstname': result[1],
                'surname': result[2],
                'email': myrow[headers['email']],
                'organization': myrow[headers['organization']],
                'phone': myrow[headers['phone']],
                'position': myrow[headers['position']]
            }
        else:
            tmp[fio]['email'] = merge(tmp[fio]['email'], myrow[headers['email']])
            tmp[fio]['organization'] = merge(tmp[fio]['organization'],  myrow[headers['organization']])
            tmp[fio]['phone'] =  merge(tmp[fio]['phone'],  myrow[headers['phone']])
            tmp[fio]['position'] =  merge(tmp[fio]['position'],  myrow[headers['position']])

    elif len(result) == 2:
        found = False
        for fio1 in tmp:
            result1 = re.match(r"^" + fi, fio1)
            if result1:
                tmp[fio1]['email'] = merge(tmp[fio1]['email'], myrow[headers['email']])
                tmp[fio1]['organization'] = merge(tmp[fio1]['organization'],  myrow[headers['organization']])
                tmp[fio1]['phone'] =  merge(tmp[fio1]['phone'],  myrow[headers['phone']])
                tmp[fio1]['position'] =  merge(tmp[fio1]['position'],  myrow[headers['position']])
                found = True
                break






#pprint(tmp)

contacts_list1 = [contacts_list[0]]
for fio in tmp:
    arr = []
    for i in range(0, len(contacts_list[0])):
        col = contacts_list[0][i]
        value = tmp[fio][col]
        if col == 'phone':
            value = re.sub(r"\s", '',  value.strip())   # +7(999)999-99-99 доб.9999.
            value = re.sub(r"^8", '+7', value)
            value = re.sub(r"^\+7(\d{3})", r'+7(\1)', value)
            value = re.sub(r"(\d{3})(\d{2})(\d{2})", r"\1-\2-\3", value)
            value = re.sub(r"(\d)(доб\.)", r" \2", value)
            value = re.sub(r"(\()(доб\.)(\d+)\)", r" \2\3", value)
        arr.append(value)
    contacts_list1.append(arr)

pprint(contacts_list1)

## 2. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')

    ## Вместо contacts_list подставьте свой список:
    datawriter.writerows(contacts_list1)
