from flask import Flask, render_template, redirect, request, session, url_for
import subprocess
import pymysql.cursors

# 初始化 Flask 应用程序
app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 创建 MySQL 数据库连接
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    database="livedata"
)

# 定义主页路由
@app.route("/home/")
def home():
    return render_template("home.html")

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/register/")
def register():
    return render_template("register.html")

# 定义登录路由
@app.route("/", methods=["POST"])
def do_login():
    username = request.form["username"]
    password = request.form["password"]

    # 检查用户是否存在
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        # 登录成功，重定向到主页
        return redirect(url_for("home"))
    else:
        # 登录失败，显示错误信息并停留在登录页面上
        error = "用户名或密码不正确。请重试或注册一个新的账号。"
        return render_template("login.html", error=error)

# 定义注册路由
@app.route("/register/", methods=["POST"])
def do_register():
    username = request.form["username"]
    password = request.form["password"]

    # 检查用户名是否以及存在
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username=%s", username)
    user = cursor.fetchone()

    if user:
        # 用户名已经存在，显示错误信息并停留在注册页面上
        error = "用户名已经存在。请换一个。"
        return render_template("register.html", error=error)

    # 添加用户到数据库
    cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cursor.close()

    # 注册成功，显示成功信息并重定向到登录页面
    success = "注册成功。你现在可以登录了。"
    return render_template("login.html", success=success)

@app.route('/douyu/')
def douyu():
    return render_template('douyu.html')

@app.route('/douyu/5/tab1')
def dy_5m_tab1():
    return render_template('dy_5m_tab1.html')

@app.route('/douyu/5/tab2')
def dy_5m_tab2():
    return render_template('dy_5m_tab2.html')

@app.route('/douyu/5/tab3')
def dy_5m_tab3():
    return render_template('dy_5m_tab3.html')

@app.route('/douyu/60')
def dy_1h():
    return render_template('dy_1h.html')

@app.route('/huya/')
def huya():
    return render_template('huya.html')

@app.route('/huya/5/tab1')
def hy_5m_tab1():
    return render_template('hy_5m_tab1.html')

@app.route('/huya/5/tab2')
def hy_5m_tab2():
    return render_template('hy_5m_tab2.html')

@app.route('/huya/5/tab3')
def hy_5m_tab3():
    return render_template('hy_5m_tab3.html')

@app.route('/huya/60')
def hy_1h():
    return render_template('hy_1h.html')


import data.dy_5m_data
import data.dy_1h_data
import data.hy_5m_data
import data.hy_1h_data
import data.clean_data
import data.dy_5m_view
import data.dy_1h_view
import data.hy_5m_view
import data.hy_1h_view


if __name__ == '__main__':
    # 调用方法：采集数据、存储数据、处理数据
    data_list = data.dy_5m_data.get_data()
    data.dy_5m_data.save_data(data_list)

    data_list = data.dy_1h_data.get_data()
    data.dy_1h_data.save_data(data_list)

    data.clean_data.clean_data('dy_5m')
    data.clean_data.clean_data('dy_1h')

    data_list = data.hy_5m_data.get_data()
    data.hy_5m_data.save_data(data_list)
    data.clean_data.clean_data('hy_5m')

    data_list = data.hy_1h_data.get_data()
    data.hy_1h_data.save_data(data_list)
    data.clean_data.clean_data('hy_1h')

    # 数据可视化
    data.dy_5m_view.render_tab('localhost', 3306, 'root', '123456', 'livedata')
    data.hy_5m_view.render_tab('localhost', 3306, 'root', '123456', 'livedata')
    data.dy_1h_view.generate_dy_1h_html()
    data.hy_1h_view.generate_hy_1h_html()

    app.run(debug=True)

