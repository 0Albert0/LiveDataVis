import pymysql
import datetime

# 对表进行数据清洗
def clean_data(table_name):
    '''
    对斗鱼数据库表进行数据清洗和预处理
    '''
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='livedata')

    # 获取游标
    cursor = conn.cursor()

    # 删除heat为0的数据
    cursor.execute("DELETE FROM {} WHERE heat = 0".format(table_name))

    # 查询表结构，获取所有字段名
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{}'".format(table_name))
    columns = cursor.fetchall()
    column_names = [column[0] for column in columns]

    # 新增start_date和start_time两个字段
    if 'start_date' not in column_names:
        cursor.execute("ALTER TABLE {} ADD start_date VARCHAR(10) AFTER start_datetime".format(table_name))
    if 'start_time' not in column_names:
        cursor.execute("ALTER TABLE {} ADD start_time VARCHAR(8) AFTER start_date".format(table_name))

    # 查询开播时间字段
    cursor.execute("SELECT start_datetime FROM {}".format(table_name))

    # 获取所有开播时间字段
    start_datetimes = cursor.fetchall()

    for start_datetime in start_datetimes:
        # 将开播时间格式转为datetime类型
        dt = datetime.datetime.strptime(start_datetime[0].replace('最近开播时间：', ''), '%Y-%m-%d %H:%M')

        # 分别提取日期和时间，并插入到对应的字段中
        cursor.execute("UPDATE {} SET start_date=%s, start_time=%s"
                       " WHERE start_datetime=%s".format(table_name),
                       [dt.strftime('%Y-%m-%d'), dt.strftime('%H:%M'), start_datetime[0]])

    # 处理gift_value字段
    if 'gift_value' in column_names:
        # 将字段中的"元"删除
        cursor.execute("UPDATE {} SET gift_value = REPLACE(gift_value, '元', '')".format(table_name))
        # 把gift_value字段的数据类型改为整数类型
        cursor.execute("ALTER TABLE {} MODIFY COLUMN gift_value INT".format(table_name))

    # 提交修改
    conn.commit()

    # 关闭游标和数据库连接
    cursor.close()
    conn.close()

