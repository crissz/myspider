import requests
from pyquery import PyQuery

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
}

def get_word_info(word):
    url = "http://dict.youdao.com/w/eng/{}/".format(word)

    resp = requests.get(url, headers=headers)

    doc = PyQuery(resp.text)

    des = ''

    print('\n单词：%s\n'%word)

    for li in doc.items('#phrsListTab > div.trans-container > ul > li'):
        print(li.text())
        des += li.text()

    print('\n')

if __name__ == '__main__':
    while True:
        word = input('请输入需要翻译的单词：')
        if word != '0':
            get_word_info(word)
        else:
            break
