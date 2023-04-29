import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


# 定义获取数据的方法
def get_data():
    # 创建浏览器对象，用于模拟浏览器操作
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # 打开目标网站
    url = 'https://bojianger.com/list-intime.html'
    driver.get(url)

    # 等待页面加载完毕，获取主播信息
    driver.implicitly_wait(10)

    data_list = []  # 定义一个列表用于存储爬取到的数据

    while True:  # 循环处理每一页的主播数据
        # 等待加载更多数据
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        driver.implicitly_wait(10)

        # 定位表格
        table = driver.find_element(By.XPATH, r'//*[@id="anchor_list_con"]')

        # 定位所有行，并对每行进行处理
        rows = table.find_elements(By.XPATH, r'./li')
        for row in rows:
            # 定位每个元素并获取其文本内容
            anchor_name    = row.find_element(By.XPATH, r'./div[1]/div/h3/a').text
            kind           = row.find_element(By.XPATH, r'./div[1]/div/p[1]').text
            link           = row.find_element(By.XPATH, './div[1]/div/p[2]/a').get_attribute('href')
            title          = row.find_element(By.XPATH, r'./div[1]/div/p[2]/a').text
            start_datetime = row.find_element(By.XPATH, r'./div[4]/span').text
            audience       = row.find_element(By.XPATH, r'./div[2]/ul/li[1]/label').text
            heat           = row.find_element(By.XPATH, r'./div[2]/ul/li[4]/label').text
            pop            = row.find_element(By.XPATH, r'./div[2]/ul/li[2]/label').text
            pop_peo        = row.find_element(By.XPATH, r'./div[2]/ul/li[5]/label').text
            gift_value     = row.find_element(By.XPATH, r'./div[2]/ul/li[3]/label').text
            gift_giver     = row.find_element(By.XPATH, r'./div[2]/ul/li[6]/label').text

            # 新增room_id字段
            room_id = link.split('/')[-1]

            # 将每个主播的信息封装为字典，加入到列表中
            data = {
                'anchor_name': anchor_name,
                'kind': kind,
                'link': link,
                'room_id': room_id,  # 新增room_id字段
                'title': title,
                'start_datetime': start_datetime,
                'audience': audience,
                'heat': heat,
                'pop': pop,
                'pop_peo': pop_peo,
                'gift_value': gift_value,
                'gift_giver': gift_giver
            }
            data_list.append(data)

        # 定位下一页按钮
        next_page_btn = driver.find_element(By.XPATH, r'/html/body/div[3]/div/ul[2]/div/a[6]')


        if 'disabled' in next_page_btn.get_attribute('class'):
            # 下一页按钮不可用，即已到达最后一页，退出循环
            break

        # 点击下一页按钮
        ActionChains(driver).move_to_element(next_page_btn).perform()
        next_page_btn.click()

    # 退出浏览器
    driver.quit()

    return data_list


# 定义存储数据的方法
def save_data(data_list):
    # 连接数据库
    db = pymysql.connect(host='localhost', user='root', password='123456', database='livedata', charset='utf8')

    # 创建游标对象
    cursor = db.cursor()

    # 判断表是否存在，如果不存在则创建新表
    cursor.execute("SELECT count(*) FROM information_schema.TABLES WHERE table_name=%s", ('dy_5m',))
    table_exists = cursor.fetchone()[0]
    if not table_exists:
        cursor.execute("CREATE TABLE dy_5m("
                       "anchor_name VARCHAR(50),"
                       "kind VARCHAR(50),"
                       "link VARCHAR(100),"
                       "room_id VARCHAR(50) PRIMARY KEY,"
                       "title VARCHAR(100),"
                       "start_datetime VARCHAR(50),"
                       "audience int,"
                       "heat int,"
                       "pop int,"
                       "pop_peo int,"
                       "gift_value VARCHAR(50),"
                       "gift_giver int"
                       ")")
    else:
        # 判断gift_value字段类型是否为int，如果是则把类型改为varchar
        cursor.execute(
            "SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='dy_5m' AND COLUMN_NAME='gift_value'")
        column_type = cursor.fetchone()[0]
        if 'int' in column_type:
            cursor.execute("ALTER TABLE dy_5m MODIFY COLUMN gift_value VARCHAR(50)")

    # 删除所有数据
    cursor.execute("DELETE FROM dy_5m")

    for data in data_list:
        # 查询表结构，获取所有字段名
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'dy_5m'")
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]

        # 如果start_datetime字段不存在，则新建该字段，并在audience字段前面
        if 'start_datetime' not in column_names:
            cursor.execute("ALTER TABLE dy_5m ADD start_datetime VARCHAR(20) AFTER title")

        # 构造插入语句
        insert_sql = f"REPLACE INTO dy_5m (anchor_name, kind, link, room_id, title, start_datetime, audience, heat, pop, pop_peo, gift_value, gift_giver) VALUES ('{data['anchor_name']}', '{data['kind']}', '{data['link']}', '{data['room_id']}', '{data['title']}', '{data['start_datetime']}', '{data['audience']}', '{data['heat']}', '{data['pop']}', '{data['pop_peo']}', '{data['gift_value']}', '{data['gift_giver']}')"

        # 执行插入语句
        cursor.execute(insert_sql)

    # 提交事务
    db.commit()

    # 关闭游标和数据库连接
    cursor.close()
    db.close()



