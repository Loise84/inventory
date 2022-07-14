
from flask import Flask, render_template ,request ,redirect, url_for
from datetime import date, datetime, time
import psycopg2
app = Flask(__name__)

#Connect to an existing database
# conn = psycopg2.connect(user="postgres", password="Chanuka84$", host="localhost", port="5432", database="myduka")
conn = psycopg2.connect(user="hunavzqoenxstn", password="c5b150105efd9fa09734424d6d41df1d4d9a015855040055a220c1f2595d8c46",host="ec2-3-234-131-8.compute-1.amazonaws.com",port="5432",database="d6q159ad9dsfb4")
#Open a cursor to perform database operations
cur = conn.cursor()


@app.route('/inventories')
def inventories():
   cur.execute("SELECT * FROM products;")
   records = cur.fetchall()
   # print(records)
   return render_template('inventories.html'  , records = records)

@app.route('/add product', methods =['POST'])
def add_product():
   productname= request.form["product_name"]
   buyingprice= request.form["buying_price"]
   sellingprice= request.form["selling_price"]
   quantity= request.form['quantity']
   cur.execute("INSERT INTO products (name, buying_price, selling_price,stock_quantity) VALUES (%s, %s, %s,%s)",(productname,buyingprice,sellingprice,quantity))
   conn.commit()
   return  redirect(url_for('inventories'))

@app.route('/makesale',methods=['POST'])
def make_sale():
   productid = request.form['pid']
   quantity = request.form['quantity']
   # cur.execute("INSERT INTO Sales (pid, quantity, created_at) VALUES (%s, %s, %s)",(productid,quantity))
   # conn.commit()
   print(productid,quantity)
   return redirect (url_for('inventories'))

@app.route('/dashboard')
def dashboard():
   cur.execute("SELECT products.name,sum(products.selling_price*sales.quantity) as total_sales FROM products INNER JOIN sales ON products.id = sales.pid GROUP BY name;")
   items= cur.fetchall()  
   labels=[]
   data = []
   
   for i in items:
      labels.append(i[0])
      data.append(int(i[1]))
   # import json
   # labels=json.dumps(labels)
   # data=json.dumps(data)
    # Push to the HTML file
   # print(labels)
   # print(data)
   
   

   cur.execute("select to_char (sales.created_at,'YYYY-MM') as sales_month,sum(sales.quantity*products.selling_price)AS amount FROM products LEFT JOIN sales ON sales.pid= products.id GROUP BY sales_month ORDER BY amount DESC;")
   records =cur.fetchall()
   records=records[1:]
   mysales1=[]
   dataline=[]

   for record in records:
        mysales1.append(record[0])
        dataline.append(float (record[1]))
   print(dataline)
   print(mysales1)
   
   return render_template("dashboard.html",labels=labels,data=data,mysales1=mysales1, dataline=dataline)
app.run()
