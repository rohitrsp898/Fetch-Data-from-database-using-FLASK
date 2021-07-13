from flask import Flask,render_template,request
from mysql import connector
import mysql.connector


app=Flask(__name__)

mydb=mysql.connector.connect(host="localhost",user="root",passwd="Root@123",auth_plugin='mysql_native_password')
cursor=mydb.cursor()


@app.route('/', methods=['GET','POST'])
def index():

    cursor.execute("show databases")
    select_db = cursor.fetchall()

    if request.method == "POST":
        selected_db=request.form['database']
        Current_db = mysql.connector.connect(host="localhost", user="root", passwd="Root@123", database=selected_db,
                                       auth_plugin='mysql_native_password')

        db_cursor = Current_db.cursor()

        db_cursor.execute("show tables")
        tables = db_cursor.fetchall()

        selected_table = request.form.get('table')

        sql_query = request.form['sql_query']


        try:  #if query inserted

            db_cursor.execute(sql_query)

            data = db_cursor.fetchall()
            field_names = [i for i in db_cursor.description]



            return render_template("index.html", tables=tables, datadb=select_db,database_name=selected_db,table_name=selected_table,query=sql_query,header=field_names,result=data)

        except:  #without query

             return render_template("index.html", tables=tables, datadb=select_db, database_name=selected_db,table_name=selected_table, query=sql_query)
    else:

        return render_template("index.html",datadb=select_db)




if __name__=="__main__":
    app.run(debug=True)

