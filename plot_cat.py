import json

import datetime

import pygal

bar_chart = pygal.Bar(x_label_rotation=90)
bar_chart.x_labels = []
json_load = json.loads(open('proces/files/cats.json', 'r').read())
for cat in json_load:
    if cat == "stufi":
        continue
    list = []
    last_date = -1
    group_amount = 0
    for transaction in json_load[cat]:
        date = datetime.datetime.strptime(transaction['date'], "%d-%m-%Y").date()
        
        if last_date == -1 or last_date.month != date.month:
            list.append(group_amount)
            last_date = date
            group_amount = transaction['amount']
            if last_date != -1 and str(date.month) + "-" + str(date.year) not in bar_chart.x_labels:
                bar_chart.x_labels.append(str(date.month) + "-" + str(date.year))
        elif last_date.month == date.month:
            group_amount += transaction['amount']
    list.append(group_amount)
    bar_chart.add(cat, list)
bar_chart.render_to_file('test.svg')
