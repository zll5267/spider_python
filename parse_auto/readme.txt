python3

依赖包:
request:提供页面http访问
安装:pip3 install requests
selenium:提供页面访问及js运行环境
安装:pip install selenium
BeautifulSoup：解析网友，提取元素
安装:pip install beautifulsoup4
selenium 对应的brower驱动:https://npm.taobao.org/mirrors/
安装:下载对应的浏览器驱动，建议chrome, 下载解压后添加到系统运行目录下

运行：
python3 get_vehicle_info.py #生成品牌/车系/车型等基本信息，访问url会根据此产生
python3 web_spider.ppy #访问对应的车型信息，提前评论数，平均评分，排名等信息

其他可以参考：
https://www.jb51.net/article/203712.htm
https://www.cnblogs.com/haifeima/p/10209635.html
https://github.com/Jack-Cherish/python-spider
