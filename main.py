import json

import pymysql.cursors

import parser

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Findus',
                             db='hunger',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        venue_sql = "SELECT id FROM venues WHERE name = %s"
        check_meal_sql = "SELECT id FROM meals WHERE name=%s"
        insert_meal_sql = "INSERT INTO meals (name) VALUE (%s)"
        insert_sql = 'REPLACE INTO menus (venue, date, meal) VALUES (%s, %s, %s)'
        for p in [parser.fladerei, parser.zuppa]:
            cursor.execute(venue_sql, p.name)
            venue_id = cursor.fetchone()["id"]
            for i in p.get_menus():
                cursor.execute(check_meal_sql, (i["name"]))
                check = cursor.fetchone()
                if check:
                    meal_id = check["id"]
                else:
                    cursor.execute(insert_meal_sql, (i["name"]))
                    meal_id = cursor.lastrowid
                cursor.execute(insert_sql, (venue_id, i["date"], meal_id))
    connection.commit()  # save changes

finally:
    connection.close()
