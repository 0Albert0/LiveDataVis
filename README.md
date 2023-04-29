# Live_Data_Visualisation_System
基于Python+Flask+Echarts的直播数据可视化系统
***
## 步骤
>* Python网络爬虫
>* 使用Python与MySQL数据库交互
>* 使用Flask构建web项目
>* 基于Echarts数据可视化展示


</br>

## 项目环境
>* Python 3.10
>* MySQL 8.0.32
>* Flask 1.1.1

## IDE
> Pycharm

</br>

## 文件说明
>* app.py是flask的运行程序，整体项目也是运行它
>* spider.py是爬取各种数据并存入数据库的，定时爬虫就是定时运行它
>* utils.py是数据库的相关操作的封装，spider.py中会调用它的函数
>* templates/中
>>* index.html和test.html是写项目过程中用于测试用的，和项目运行无关，可删
>>* main.html是前端页面

## 运行方式：
> ### **本地win11上:**
	在mysql数据库中新建cov数据库，并在其中新建3张表details,history,hotsearch
	在utils.py和spider.py中更改get_conn函数中的数据库连接，host,user,password，db 
	运行spider.py爬取数据写入到mysql中
	运行app.py