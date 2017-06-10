import logging

from flask import Flask, jsonify, url_for, redirect, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{user}:{password}@{host}/{db}?unix_socket=/var/run/mysqld/mysqld.sock".format(**config.db)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)


@app.route('/api/venue/')
def get_venues():
    sql = text("SELECT * FROM venues")
    results = db.engine.execute(sql).fetchall()
    venues = []
    for row in results:
        venue = dict(row)
        venue["meals_url"] = url_for("get_meals", venueid=venue["id"], _external=True)
        venues.append(venue)
    return jsonify(venues)


@app.route('/api/venue/<int:venueid>/')
def get_meals(venueid):
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
WHERE venue = :venue"""
    results = db.engine.execute(text(sql + sql_range), {"venue": venueid}).fetchall()
    menus = []
    for row in results:
        menu = dict(row)
        menu["date"] = menu["date"].isoformat()
        menus.append(menu)
    return jsonify(menus)


@app.route("/api/")
def redirect_to_correct_api():
    return redirect(url_for("get_venues"))


if __name__ == "__main__":
    app.run(debug=True)
