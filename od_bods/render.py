from jinja2 import Environment, FileSystemLoader
import csv

data = []

with open("../data/arcgis/moray.csv") as f:
    r = csv.reader(f)
    headers = r.__next__()
    for d in r:
        data.append(d)

env = Environment(loader=FileSystemLoader("."))
template = env.get_template('table.html')
page = template.render(data=data, headers=headers)

with open("rendered_table.html", "w") as f:
    f.write(page)
