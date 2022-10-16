#excelにデータを出力するファイル
import requests
import bs4
#１問目
#指定のURLのwebページの情報を取得
html = requests.get("https://www.jara.co.jp/member_list/")
#HTMLを解析する
soup = bs4.BeautifulSoup(html.content,'lxml')
#空の配列の作成
data = []
#クラスがarticle_innerのHTML要素を全て取得し、その数だけループ下のち、さらにその子要素のtrタグの数だけループ
for script in soup.find_all(class_='article_innner'):
  for value in script.find_all('tr'):
    #area=地域名、company=会社名、adress=住所、tel=電話番号を取得し配列にそれぞれ追加
    area = script.find('h3').text
    company = value.find_all('td')[0].text
    adress = value.find_all('td')[1].text
    tel = value.find_all('td')[2].text
    data.append([area,company,adress,tel])
import pandas as pd
#配列をexcelに出力するためのデータフレームに格納
df = pd.DataFrame(data,columns=['都道府県','会社名','住所','電話番号'])

#2問目
html5 = requests.get("https://www.i-parts.co.jp/used/index.asp?",
                   params={'rs' : '0','pcm' : '7'})
soup5 = bs4.BeautifulSoup(html5.content,'lxml')
data5 = []
#summary="result"のテーブルタグを取得しその子要素のtrタグの分だけループ
table5 = soup5.find('table',summary="result")
for script5 in table5.find_all('tr'):
    #name=商品名、car=適合車種名称、code=商品コード、price=価格、store=取り扱い店舗を取得し配列にそれぞれ追加
    if script5.find('td') is not None:
     name = script5.find_all('td')[1].find('a').text
     #商品詳細ページのURLを取得
     url = script5.find_all('td')[1].find('a').get('href')
     html2 = requests.get('https://www.i-parts.co.jp/' + url)
     soup2 = bs4.BeautifulSoup(html2.content , 'lxml')
     table2 = soup2.find('table',summary="spec")
     #7番目のtrタグの子要素のtdタグを取得
     car = table2.find_all('tr')[6].find('td').text          
     for value in script5.find_all('td')[1].find('p'):
        #「番号:」という記述を削除
        code = value[3::]
     price = script5.find_all('td')[2].text
     store = script5.find_all('td')[3].text
     data5.append([name,price,store,code,car])
#配列をexcelに出力するためのデータフレームに格納
df5 = pd.DataFrame(data5,columns=['商品名','価格','取り扱い店舗','商品コード','適合車種名称'])

#出力するファイル名を'ponta.xlsx'としてwriterを定義
writer = pd.ExcelWriter('/Users/maceponta/Downloads/ponta.xlsx', engine = 'xlsxwriter')
#1問目をexcelのシートのtest1に出力
df.to_excel(writer,sheet_name='test1',index=False)
#2問目をexcelのシートのtest2に出力
df5.to_excel(writer,sheet_name='test2',index=False)
#excelファイルを保存
writer.save()