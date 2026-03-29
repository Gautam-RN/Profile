from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='profile',
        charset="utf8"
    )
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['mail']
    msg = request.form['msg']
    phone = request.form['phone']
    tup=(name,email,msg,phone)
    
    cursor.execute("INSERT INTO messages VALUES (%s,%s,%s,%s)", tup)
    conn.commit()
    
    return render_template('msg.html')

@app.route('/projects')
def products():
    return render_template('products.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/project-view')
def projview():
    code=request.args.get('code')
    try:
        cursor.execute('Select * from projects where code=%s',(code,))
    except:
        return render_template('wrong.html')
    data=cursor.fetchone()
    project=data[1:]
    return render_template('each.html', project=project)

@app.route("/add")
def addwindow():
    return render_template("update.html")

@app.route('/add-product', methods=["POST"])
def add():
    name = request.form['name']
    desc = request.form['description']
    url = request.form['url']
    img = request.form['imgurl']
    use = request.form['use']
    cursor.execute("Select * from projects")
    data=cursor.fetchall()
    i=len(data)+1
    tup=(i,name,desc,url,img,use)
    cursor.execute("INSERT INTO projects VALUES (%s,%s,%s,%s,%s,%s);", tup)
    conn.commit()
    
    return f"Update success: {tup}"

if __name__ == '__main__':
    app.run(debug=True)

conn.close()
