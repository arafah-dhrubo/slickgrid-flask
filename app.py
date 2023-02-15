import json

from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine, text

app = Flask(__name__)
engine = create_engine('postgresql+psycopg2://postgres:1@localhost:5432/stockdb')
connection = engine.connect()


@app.route("/")
def index():
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

    return render_template("example-grid-menu.html", fields=columns, list=data)


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
