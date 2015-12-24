import json
import datetime
import os

import requests
from parse_login_html import *
from sqlalchemy import MetaData


def login():
    login_url = 'https://mijn.ing.nl/internetbankieren/SesamLoginServlet'
    url_overview = 'https://bankieren.mijn.ing.nl/particulier/betalen/index'

    from config import ing_password, ing_username

    session = requests.Session()

    login_page = session.get(login_url)
    username_id = get_username_id(login_page.text)
    password_id = get_password_id(login_page.text)
    deviceprint_id = get_deviceprint_id(login_page.text)

    payload = {
        username_id: ing_username,
        password_id: ing_password,
        deviceprint_id: 'version%3D2%26pm%5Ffpua%3Dmozilla%2F5%2E0%20%28x11%3B%20linux%20x86%5F64%29%20applewebkit%2F537%2E36%20%28khtml%2C%20like%20gecko%29%20chrome%2F47%2E0%2E2526%2E106%20safari%2F537%2E36%7C5%2E0%20%28X11%3B%20Linux%20x86%5F64%29%20AppleWebKit%2F537%2E36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F47%2E0%2E2526%2E106%20Safari%2F537%2E36%7CLinux%20x86%5F64%26pm%5Ffpsc%3D24%7C1440%7C900%7C876%26pm%5Ffpsw%3D%26pm%5Ffptz%3D1%26pm%5Ffpln%3Dlang%3Den%2DUS%7Csyslang%3D%7Cuserlang%3D%26pm%5Ffpjv%3D0%26pm%5Ffpco%3D1%26pm%5Ffpasw%3Dmhjfbmdgcfjbbpaeojofohoefgiehjai%7Clibpepflashplayer%7Clibwidevinecdmadapter%7Cinternal%2Dnacl%2Dplugin%7Cinternal%2Dpdf%2Dviewer%26pm%5Ffpan%3DNetscape%26pm%5Ffpacn%3DMozilla%26pm%5Ffpol%3Dtrue%26pm%5Ffposp%3D%26pm%5Ffpup%3D%26pm%5Ffpsaw%3D1440%26pm%5Ffpspd%3D24%26pm%5Ffpsbd%3D%26pm%5Ffpsdx%3D%26pm%5Ffpsdy%3D%26pm%5Ffpslx%3D%26pm%5Ffpsly%3D%26pm%5Ffpsfse%3D%26pm%5Ffpsui%3D',
        'lptr': '{"v4a":{"r":"0"},"v4b":{"f":"0"},"v7":{"s":""},"v4":{"j":""},"timestamp":"2015-12-22 17:26:15","ki":"1","v6":{"u":"","k":""}}',
        'lpts': 'f4683cac348da8a8c1b834d7844cb67a412909a056b45b9c92692a6a1b61fb6b'
    }
    r = session.post(login_url, data=payload)
    if url_overview in r.text:
        return session
    return False


def download_transactions():
    url_transactions = 'https://bankieren.mijn.ing.nl/api/g-payments/search?df=01-01-2000'

    session = login()
    if session is False:
        return False

    r = session.get(url_transactions)

    json_data = json.loads(r.text[5:])
    transactions = json_data['transactions']

    for transaction in transactions:
        statements = []
        for line in transaction['statementLines']:
            statements.append(line.strip())
        statements = ' '.join(statements)
        transaction['statements'] = statements

    return transactions


def init_transactions():
    from database import db_session
    from models import Transaction

    Transaction.query.delete()

    transactions = download_transactions()
    if not transactions:
        print("Login fail")
        exit()

    for transaction in transactions:
        db_session.add(
            Transaction(datetime.datetime.strptime(transaction['date'], "%d-%m-%Y").date(),
                        transaction['type'],
                        transaction['amount'],
                        transaction['statements']
                        )
        )
    db_session.add(
        Transaction(datetime.datetime.strptime("01-01-2006", "%d-%m-%Y").date(),
                    "BA",
                    "-30.19",
                    "Kalibratie")
    )
    db_session.commit()


def ing_get_saldo():
    url_accounts = "https://bankieren.mijn.ing.nl/api/g-payments/accounts"

    session = login()
    if session is False:
        return False
    r = session.get(url_accounts)
    json_accounts = json.loads(r.text[5:])
    return json_accounts['totalBalanceOrBudget']
