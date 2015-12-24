import datetime
import json

from charts.line_chart import line_chart
from database import init_db, db_session
from flask import Flask, render_template, request, redirect, url_for, jsonify
from ing_handler import init_transactions, ing_get_saldo
from models import Transaction, Tag
from sqlalchemy import func

app = Flask(__name__)

init_db()


@app.route("/")
def hello():
    return render_template('transactions.html')


@app.route("/tags")
def tags():
    return render_template('tags.html', tags=Tag.query.all())


@app.route("/api/new_tag", methods=['POST'])
def new_tag():
    print(request)
    t = Tag(request.form['name'], request.form['color'])
    db_session.add(t)
    db_session.commit()
    return redirect(url_for('tags'))


@app.route("/api/get_saldo")
def get_saldo():
    t_saldo = Transaction.get_saldo()
    ing_saldo = ing_get_saldo()
    if t_saldo is False or ing_saldo is False:
        return "ERROR", 502
    return json.dumps(
        {
            "t_saldo": float(t_saldo),
            "ing_saldo": ing_saldo
        }
    ), 200


@app.route("/api/update_database")
def update_database():
    init_transactions()
    res = Transaction.query.order_by(Transaction.date.desc()).limit(20)
    return jsonify(json_list=[i.serialize for i in res])


@app.route("/api/get_transactions/<int:start>/<int:stop>")
def get_transactions(start, stop):
    res = Transaction.query.order_by(Transaction.date.desc()).slice(start, stop)
    return jsonify(json_list=[i.serialize for i in res])


@app.route("/api/chart/current_month")
def chart_cmonth():
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    print(last_month)
    saldo = float(Transaction.get_saldo(end_date=last_month))
    values = db_session.query(Transaction.date, func.sum(Transaction.amount).label('amount')). \
        filter(Transaction.date > last_month). \
        group_by(Transaction.date).all()
    saldo_values = []
    for v in values:
        saldo += float(v.amount)
        saldo_values.append((v.date, saldo))
    return line_chart(saldo_values, "Saldo")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
