import json


def has_attribute(transaction, k):
    return k in transaction.keys()


def parse_filter(transaction, k, v):
    if v[0] == "e":
        return transaction[k].lower() == v[1].lower()
    elif v[0] == "c":
        return v[1].lower() in transaction[k].lower()
    elif v[0] == "m":
        return transaction[k] >= v[1]
    elif v[0] == "l":
        return transaction[k] <= v[1]


def pass_filters(transaction, filters):
    for k, v in filters.items():
        if not has_attribute(transaction, k) or not parse_filter(transaction, k, v):
            return False
    return True


def add_to_categorie(transaction, cat, filter_result):
    if cat in filter_result.keys():
        filter_result[cat].append(transaction)
    else:
        filter_result[cat] = [transaction]
