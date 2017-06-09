from datetime import date
from pprint import pprint

import pymysql
from flask import Flask, jsonify, url_for, redirect, request, abort
from flask.json import JSONEncoder

app = Flask(__name__)
import config

# Connect to the database
connection = pymysql.connect(host=config.host,
                             user=config.user,
                             password=config.password,
                             db=config.db,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/venue/')
def get_venues():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM venues"
        cursor.execute(sql)
        venues = cursor.fetchall()
        for venue in venues:
            # venue["meals_url"] = url_for("get_meals", venueid=venue["id"])
            venue["meals_url"] = url_for("get_meals", venueid=venue["id"], _external=True)
        return jsonify(venues)


@app.route('/venue/<int:venueid>/')
def get_meals(venueid):
    with connection.cursor() as cursor:
        select = request.args.get("select")
        if not select or select == "week":
            sql_range = " AND YEARWEEK(date, 1) = YEARWEEK(CURDATE(), 1)"
        elif select == "today":
            sql_range = " AND date=CURDATE()"
        else:
            return abort(400)
        sql = """SELECT venue, date, name, description
FROM menus
  JOIN meals ON meals.id = menus.meal
WHERE venue = %s"""
        cursor.execute(sql + sql_range, venueid)
        menues = cursor.fetchall()
        return jsonify(menues)


@app.route("/")
def redirect_to_correct_api():
    return redirect(url_for("get_venues"))


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder


if __name__ == "__main__":
    app.json_encoder = CustomJSONEncoder
    app.run(host="0.0.0.0", debug=True)
