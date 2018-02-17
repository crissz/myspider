import re, pymysql
from pyquery import PyQuery as pq

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
}

#爬取数据函数
def get_code():
    #初始爬取页码
    page_no = 1
    #初始总页数
    total_page = 1
    #预定义返回列表
    res_data = []

    #循环爬取开始，条件为当前页码小于等于总页数
    while page_no <= total_page:
        #爬取url,并获取当前页面除标记外字符串内容
        url = 'http://kaijiang.zhcw.com/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum='+str(page_no)
        res = pq(url, headers=headers).text()
        #预定义返回的当前页面数据列表
        res_pre = []
        #获得总页数
        re_total = re.search(r'共\s(\d+?)\s页',res) 
        total_page = int(re_total.group(1))
        #开始爬取当前页，以正则获得数据，做一些转换整理后，生成当前页数据列表
        re_res = re.findall(r'(20\d{2}-\d{2}-\d{2})\s(\d{7})\s(\d{2})\s(\d{2})\s(\d{2})\s(\d{2})\s(\d{2})\s(\d{2})\s(\d{2})\s(.+?)\s(\d{1,3}).*?\s(\d{1,8})',res)
        for r in re_res:
            r = list(r)
            r[9] = r[9].replace(',','')
            res_pre.append(r)
        #当前页数据列表追加入返回列表
        res_data.extend(res_pre)
        #增加页码，开始下一页循环
        page_no += 1
    #返回获取数据总表
    return res_data

#写入本地文件
def insert_file(res_data):
    with open('file.txt', 'w') as writer:
        for ps in res_data:
            writer.write(','.join(ps)+'\n')

#写入mysql数据库
def insert_data(res_data):
    db = pymysql.connect("10.0.0.2","root","数据库密码","lottery")
    cursor = db.cursor()
    
    #表字段可参考以下sql语句
    for p in res_data:
        sql = "INSERT INTO doublecolorball(date,period,red_1,red_2,red_3,red_4,red_5,red_6,blue,sales,first,second) \
        VALUES('%s','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%d')" \
        %(p[0],int(p[1]),int(p[2]),int(p[3]),int(p[4]),int(p[5]),int(p[6]),int(p[7]),int(p[8]),int(p[9]),int(p[10]),int(p[11]))
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    db.close()

if __name__ == '__main__':
    rs = get_code()
    insert_file(rs)
    #最后打印一下总获取写入行数
    print(len(rs))
