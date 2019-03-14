# gaokao
爬取高考网广东省内高校信息、各高校往年分数线
链接: http://college.gaokao.com/schlist/a14/p1/
本章主要介绍下简单的爬取，不采用任何框架，只爬取广东省内的高校，让读者能对requests的请求方式,正则表达式与xpath的解析方式,json与MYSQL的存取方式有一定了解。
首先需要先运行gaokao_mysql_1.py创建一个数据库
再者就是运行gaokao_myssql_2.py创建需要的数据表
这里我们将高校基本信息存入数据库中
而高校往年文理科分数线存为json格式
