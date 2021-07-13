#Required modules 
from flask import Flask,render_template,request
from mysql import connector
import mysql.connector


app=Flask(__name__)

#connect to MySQL Database
mydb=mysql.connector.connect(host="localhost",user="User_name",passwd="#user_password",auth_plugin='mysql_native_password')
cursor=mydb.cursor()

#get post 
@app.route('/', methods=['GET','POST'])
def index():

    #get all the database from MYSQL
    cursor.execute("show databases")
    select_db = cursor.fetchall()           #Store the database name in select_db variable

    #POST method
    if request.method == "POST":
        
        #dropdown selected database HTML
        selected_db=request.form['database']
        Current_db = mysql.connector.connect(host="localhost", user="User_name",passwd="#user_password", database=selected_db,
                                       auth_plugin='mysql_native_password')
        #selected database cursor
        db_cursor = Current_db.cursor()
        
        #get all the tables from selected database
        db_cursor.execute("show tables")
        tables = db_cursor.fetchall()

        #dropdown selected table from HTML
        selected_table = request.form.get('table')
        
        #SQL Query from textarea from HTML
        sql_query = request.form['sql_query']

        #If SQL Query from textarea is inserted
        try:  

            db_cursor.execute(sql_query)                        #Firing SQL Query from HTML
            data = db_cursor.fetchall()                         #Based on query get all the data from table and stored in "data" variable
            field_names = [i for i in db_cursor.description]    #Store Column name of the Query in "field_names"



            return render_template("index.html", tables=tables, datadb=select_db,database_name=selected_db,table_name=selected_table,query=sql_query,header=field_names,result=data)

        except:  #If SQL Query not inserted

             return render_template("index.html", tables=tables, datadb=select_db, database_name=selected_db,table_name=selected_table, query=sql_query)
            
    else: #GET Method

        return render_template("index.html",datadb=select_db)



# main 
if __name__=="__main__":
    app.run(debug=True)

