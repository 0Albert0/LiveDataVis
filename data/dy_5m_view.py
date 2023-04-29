from pyecharts.charts import Tab, Bar
from pyecharts import options as opts
import pymysql
from pyecharts.commons.utils import JsCode


def render_tab(host, port, user, password, database):
    # 在选项卡的标题上添加一个返回按钮
    back_button = """
    <button style='position: absolute; right: 10px; top: 10px' onclick=window.location.href='/douyu/'>返回</button>
    """

    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)

    # 取总热度前10的直播类型来分组，绘制水平条形图
    cursor = conn.cursor()
    sql = """
        SELECT kind, SUM(heat) AS total_heat
        FROM dy_5m
        GROUP BY kind
        ORDER BY total_heat DESC
        LIMIT 10
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    kind_lst = [item[0] for item in results]
    bar_lst = []

    for kind in kind_lst:
        sql_list = [
            f"SELECT anchor_name, audience, heat FROM dy_5m WHERE kind = '{kind}' ORDER BY audience ",
            f"SELECT anchor_name, audience, heat FROM dy_5m WHERE kind = '{kind}' ORDER BY heat "
        ]
        for sql in sql_list:
            cursor.execute(sql)
            anchor_results = cursor.fetchall()
            anchor_lst = [f"{item[0]}" for item in anchor_results]
            audience_lst = [item[1] for item in anchor_results]
            heat_lst = [item[2] for item in anchor_results]

            bar = (
                Bar()
                .add_xaxis(anchor_lst)
                .add_yaxis("观看人数", audience_lst, category_gap="60%")
                .add_yaxis("观看热度", heat_lst, category_gap="60%")
                .reversal_axis()
                .set_global_opts(title_opts=opts.TitleOpts(title=f"{kind} 人气情况"))
            )

        bar_lst.append(bar)

    cursor.close()

    # 将多个图表整合为一个选项卡
    tab1 = Tab()
    for i in range(len(bar_lst)):
        if i == 0:
            tab1.add(bar_lst[i], f"总热度前10的分区:{kind_lst[i]}" + back_button)
        else:
            tab1.add(bar_lst[i], f"{kind_lst[i]} ")

    # 取观看人数前10的直播类型来分组，绘制水平条形图
    cursor = conn.cursor()
    sql = """
        SELECT kind, SUM(audience) AS total_audience
        FROM dy_5m
        GROUP BY kind
        ORDER BY total_audience DESC
        LIMIT 10
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    kind_lst = [item[0] for item in results]
    bar_lst2 = []

    for kind in kind_lst:
        sql_list = [
            f"SELECT anchor_name, pop, pop_peo FROM dy_5m WHERE kind = '{kind}' ORDER BY pop ",
            f"SELECT anchor_name, pop, pop_peo FROM dy_5m WHERE kind = '{kind}' ORDER BY pop_peo  "
        ]
        for sql in sql_list:
            cursor.execute(sql)
            anchor_results = cursor.fetchall()
            anchor_lst = [f"{item[0]}" for item in anchor_results]
            pop_lst = [item[1] for item in anchor_results]
            pop_peo_lst = [item[2] for item in anchor_results]

            bar = (
                Bar()
                .add_xaxis(anchor_lst)
                .add_yaxis("弹幕数量", pop_lst, category_gap="60%")
                .add_yaxis("发弹幕人数", pop_peo_lst, category_gap="60%")
                .reversal_axis()
                .set_global_opts(title_opts=opts.TitleOpts(title=f"{kind} 弹幕情况"))
            )

        bar_lst2.append(bar)

    cursor.close()

    # 将多个图表整合为一个选项卡
    tab2 = Tab()
    for i in range(len(bar_lst)):
        if i == 0:
            tab2.add(bar_lst2[i], f"总观看人数前10的分区:{kind_lst[i]} " + back_button)
        else:
            tab2.add(bar_lst2[i], f"{kind_lst[i]} ")

    # 取礼物总值前10的直播类型来分组，绘制水平条形图
    cursor = conn.cursor()
    sql = """
        SELECT kind, SUM(gift_value) AS total_gift_value
        FROM dy_5m
        GROUP BY kind
        ORDER BY total_gift_value DESC
        LIMIT 10
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    kind_lst = [item[0] for item in results]
    bar_lst3 = []

    for kind in kind_lst:
        sql_list = [
            f"SELECT anchor_name, gift_giver, gift_value FROM dy_5m WHERE kind = '{kind}' ORDER BY gift_giver ",
            f"SELECT anchor_name, gift_giver, gift_value FROM dy_5m WHERE kind = '{kind}' ORDER BY gift_value "
        ]
        for sql in sql_list:
            cursor.execute(sql)
            anchor_results = cursor.fetchall()
            anchor_lst = [f"{item[0]}" for item in anchor_results]
            gift_giver_lst = [item[1] for item in anchor_results]
            gift_value_lst = [item[2] for item in anchor_results]

            bar = (
                Bar()
                .add_xaxis(anchor_lst)
                .add_yaxis("送礼人数", gift_giver_lst, category_gap="60%")
                .add_yaxis("礼物总值", gift_value_lst, category_gap="60%")
                .reversal_axis()
                .set_global_opts(title_opts=opts.TitleOpts(title=f"{kind} 礼物情况"))
            )

        bar_lst3.append(bar)

    cursor.close()

    # 将多个图表整合为一个选项卡
    tab3 = Tab()
    for i in range(len(bar_lst)):
        if i == 0:
            tab3.add(bar_lst3[i], f"礼物总值前10的分区:{kind_lst[i]} " + back_button)
        else:
            tab3.add(bar_lst3[i], f"{kind_lst[i]} ")

    tab1.render("./templates/dy_5m_tab1.html")
    tab2.render("./templates/dy_5m_tab2.html")
    tab3.render("./templates/dy_5m_tab3.html")

