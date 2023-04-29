import pymysql
from pyecharts import options as opts
from pyecharts.charts import Pie, Tab
from pyecharts.commons.utils import JsCode


def generate_dy_1h_html():
    # 连接数据库
    db = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='livedata')

    # 查询总热度前10的直播类型
    cursor = db.cursor()
    sql = "SELECT kind, COUNT(room_id) as anchor_count, SUM(audience) as total_audience" \
          " FROM dy_1h GROUP BY kind ORDER BY SUM(heat) DESC LIMIT 10"
    cursor.execute(sql)
    result = cursor.fetchall()
    kind_data = [i[0] for i in result]

    anchor_count_data = [i[1] for i in result]
    # 使用饼图展示主播数量占比
    pie1 = (
        Pie()
        .add("", [list(z) for z in zip(kind_data, anchor_count_data)], center=["50%", "50%"])
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{d}%", position="inside"))
        .set_global_opts(title_opts=opts.TitleOpts(title="热度前10分区", subtitle="主播数量占比"))
    )

    total_audience_data = [i[2] for i in result]
    # 使用饼图展示观众占比
    pie2 = (
        Pie()
        .add("", [list(z) for z in zip(kind_data, total_audience_data)], center=["50%", "50%"])
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{d}%", position="inside"))
        .set_global_opts(title_opts=opts.TitleOpts(title="热度前10分区", subtitle="观看人数占比"))
    )

    # 查询总观看人数前10的直播类型
    sql = "SELECT kind, SUM(audience) as total_audience, SUM(pop) AS total_pop, SUM(pop_peo) AS total_pop_peo, SUM(gift_value) as total_gift_value, sum(gift_giver)as total_gift_giver FROM dy_1h GROUP BY kind ORDER BY total_audience DESC LIMIT 10"
    cursor.execute(sql)
    result = cursor.fetchall()
    kind_data = [i[0] for i in result]

    total_pop_data = [i[2] for i in result]
    total_pop_peo_data = [i[3] for i in result]

    # 使用饼图展示这10个类型的弹幕数量和发弹幕人数占比
    # 将弹幕数量和发弹幕人数放在同一个图表里面
    pie3 = (
        Pie()
        .add("弹幕数量", list(zip(kind_data, total_pop_data)), center=["30%", "55%"])
        .add("发弹幕人数", list(zip(kind_data, total_pop_peo_data)), center=["70%", "55%"])
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{d}%", position="inside"))
        .set_global_opts(title_opts=opts.TitleOpts(title="弹幕数量-弹幕人数占比"),
                         legend_opts=opts.LegendOpts(pos_left="18%"))
    )

    total_gift_value_data = [i[4] for i in result]
    total_gift_giver_data = [i[5] for i in result]

    # 使用饼图展示这10个类型的礼物总值和送礼物人数占比
    # 将礼物总值和送礼物人数放在同一个图表里面
    pie4 = (
        Pie()
        .add("礼物总值", list(zip(kind_data, total_gift_value_data)), center=["30%", "55%"])
        .add("送礼人数", list(zip(kind_data, total_gift_giver_data)), center=["70%", "55%"])
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{d}%", position="inside"))
        .set_global_opts(title_opts=opts.TitleOpts(title="礼物总值-送礼人数占比"),
                         legend_opts=opts.LegendOpts(pos_left="18%"))
    )

    # 在选项卡的标题上添加一个返回按钮
    back_button = """
    <button style='position: absolute; right: 10px; top: 10px' onclick=window.location.href='/douyu/'>返回</button>
    """

    # 将pie放在同一个选项卡里面
    tab = Tab()
    tab.add(pie1, "主播数量")
    tab.add(pie2, "观看人数")
    tab.add(pie3, "弹幕情况")
    tab.add(pie4, "礼物情况" + back_button)

    # 保存为HTML文件
    tab.render("./templates/dy_1h.html")


if __name__ == '__main__':
    generate_dy_1h_html()
