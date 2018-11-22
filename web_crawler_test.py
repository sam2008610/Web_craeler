import requests


def get_web_page(url):
    resp = requests.get(
        url = url,
        cookies={'over18':'1'}
    )
    if resp.status_code !=200: #statu_code取得 server 回覆的狀態碼 200 表示正常, 404 表示找不到網頁等
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text
if __name__ == '__main__':
    page = get_web_page('https://www.ptt.cc/bbs/Beauty/index.html')
    

#檔案輸入輸出
# f = open('D:/test.txt','w',encoding='UTF-8' )
# f.write(page)
# f.close
