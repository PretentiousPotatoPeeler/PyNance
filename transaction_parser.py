import json

from proces import pass_filters, add_to_categorie

filter_result = {}


def parse_transaction(transaction):
    all_filters = json.loads(open("proces/filters.json", 'r').read())
    for filter in all_filters:
        if pass_filters(transaction, filter['filters']):
            add_to_categorie(transaction, filter['name'], filter_result)


def output_filter_result():
    f = open('proces/files/cats.json', 'w')
    f.write(json.dumps(filter_result))
    f.close()
