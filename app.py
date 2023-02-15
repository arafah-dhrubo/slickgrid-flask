import json
import requests

from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine, text

app = Flask(__name__)
engine = create_engine('postgresql+psycopg2://postgres:1@localhost:5432/stockdb')
connection = engine.connect()


@app.route("/backup")
def backup():
    query_for_header = f"SELECT column_name FROM information_schema.columns WHERE table_name = 'company'"
    fields = connection.execute(text(query_for_header))

    # construct SELECT statement
    headers = [field[0] for field in fields]
    columns = ", ".join(headers)
    query_for_all = f'SELECT {columns} FROM company'

    columns = []
    for header in headers:
        column = {'id': header, 'name': header, 'field': header, "width": 160, "resizable": True, "selectable": True,
                  "sortable": False, "editor": "Slick.Editors.Text"}
        columns.append(column)

    list = connection.execute(text(query_for_all)).fetchall()
    data = [{headers[i]: tup[i] for i in range(len(headers))} for tup in list]
    print(fields)
    return render_template("example-grid-menu.html", fields=columns, list=data)


@app.route("/")
def index():
    response = requests.get('http://localhost:5501/shared/loadscreener/')

    if response.status_code == 200:  # Check if the request was successful
        json_data = response.json()
        bbo_list = json_data['bbo_list']
        ltp_list = json_data['ltp_list']
        symbol_info_list = json_data['symbol_info_list']
    else:
        print(f"Failed to retrieve data: {response.status_code}")

    columns = [
        {
            "editor": "Slick.Editors.Text",
            "field": "id",
            "id": "id",
            "name": "id",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "symbol",
            "id": "symbol",
            "name": "symbol",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "company_name",
            "id": "company_name",
            "name": "Name",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "sector",
            "id": "sector",
            "name": "sector",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },{
            "editor": "Slick.Editors.Text",
            "field": "ltp",
            "id": "ltp",
            "name": "ltp",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },{
            "editor": "Slick.Editors.Text",
            "field": "ycp",
            "id": "ycp",
            "name": "ycp",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "total_qty",
            "id": "total_qty",
            "name": "Volume",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },{
            "editor": "Slick.Editors.Text",
            "field": "ltp_change",
            "id": "ltp_change",
            "name": "Chg",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },{
            "editor": "Slick.Editors.Text",
            "field": "ltp_changeper",
            "id": "ltp_changeper",
            "name": "% Chg",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "bid_price",
            "id": "bid_price",
            "name": "bid_price",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "bid_qty",
            "id": "bid_qty",
            "name": "bid_qty",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "ask_price",
            "id": "ask_price",
            "name": "ask_price",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "ask_qty",
            "id": "ask_qty",
            "name": "ask_qty",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "total_trades",
            "id": "total_trades",
            "name": "Trades",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "total_value",
            "id": "total_value",
            "name": "total_value",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "open",
            "id": "open",
            "name": "open",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "high",
            "id": "high",
            "name": "high",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
        {
            "editor": "Slick.Editors.Text",
            "field": "low",
            "id": "low",
            "name": "low",
            "resizable": "true",
            "selectable": "true",
            "sortable": "false",
            "width": 160
        },
    ]

    symbol_dict = {item['symbol']: item for item in bbo_list}
    for item in ltp_list:
        symbol_dict.get(item['symbol'], {}).update(item, inplace=True)

    combined_list = list(symbol_dict.values())

    combined_dict = {item['symbol']: item for item in combined_list}
    for item in symbol_info_list:
        if item['symbol'] in combined_dict:
            combined_dict[item['symbol']].update(item, inplace=True)

    combined_list = list(combined_dict.values())

    return render_template("example-grid-menu.html", fields=columns, list=combined_list)


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/example-header-row")
def example_header_row():
    query_for_header = f"SELECT column_name FROM information_schema.columns WHERE table_name = 'company'"
    fields = connection.execute(text(query_for_header))

    # construct SELECT statement
    headers = [field[0] for field in fields]
    columns = ", ".join(headers)
    query_for_all = f'SELECT {columns} FROM company'

    columns = []
    for header in headers:
        column = {'id': header, 'name': header, 'field': header, "width": 160, "resizable": True, "selectable": True,
                  "sortable": False, "editor": "Slick.Editors.Text"}
        columns.append(column)

    list = connection.execute(text(query_for_all)).fetchall()
    data = [{headers[i]: tup[i] for i in range(len(headers))} for tup in list]
    return render_template("example-header-row.html", fields=columns, list=data)


@app.route("/example4-model")
def example4_model():
    query_for_header = f"SELECT column_name FROM information_schema.columns WHERE table_name = 'company'"
    fields = connection.execute(text(query_for_header))

    # construct SELECT statement
    headers = [field[0] for field in fields]
    columns = ", ".join(headers)
    query_for_all = f'SELECT {columns} FROM company'

    columns = []
    for header in headers:
        column = {'id': header, 'name': header, 'field': header,
                  "behavior": "select", "cannotTriggerInsert": False,
                  "cssClass": "cell-selection", "defaultSortAsc": True,
                  "excludeFromColumnPicker": True, "focusable": True,
                  "headerCssClass": True, "minWidth": 30, "rerenderOnResize": True, "resizable": True,
                  "selectable": True, "sortable": True, "width": 140, "widthRequest": 60
                  }
        columns.append(column)

    list = connection.execute(text(query_for_all)).fetchall()
    data = [{headers[i]: tup[i] for i in range(len(headers))} for tup in list]
    return render_template("example4-model.html", fields=columns, list=data)


@app.route("/update-company", methods=["POST"])
def update_company():
    query_for_update = f"UPDATE company SET dse_name = '{request.form['dse_name']}', investing_name = '{request.form['investing_name']}', investing_pid = '{request.form['investing_pid']}', investing_url = '{request.form['investing_url']}', name='{request.form['name']}'  WHERE id = '{request.form['id']}'"
    connection.execute(text(query_for_update))
    connection.commit()
    return jsonify(
        status="Success",
        code=200
    )
