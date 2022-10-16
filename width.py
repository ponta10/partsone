セルの最大幅を調節するファイル
import openpyxl as xl

#1→A,2→B,3→Cというように数字をアルファベットに変換する関数
def toAlpha2(num):
    i = int((num-1)/26)
    j = int(num-(i*26))
    Alpha = ''
    for z in i,j:
        if z != 0:
            Alpha += chr(z+64)
    return Alpha

inputfile = '/Users/maceponta/Downloads/ponta.xlsx'
wb1.save(inputfile)
#excelファイルの読み込み
wb1 = xl.load_workbook(filename=inputfile)
#2回繰り返す
for counter in range(2):
    #1回目：test1,2回目:test2
    ws1 = wb1[f'test{counter+1}']
    #列の最大幅に合わせる
    for col in ws1.columns:
     max_length = 0
     column = col[0].column
     #これまでの最大幅と現在の幅を比較して現在の幅が大きたかったら、最大幅をその幅に更新
     for cell in col:
      if len(str(cell.value)) > max_length:
       max_length = len(str(cell.value))
      #少しゆとりを持たせてセルの幅を調整する
      adjusted_width = (max_length + 5) * 1.4
      ws1.column_dimensions[toAlpha2(column)].width = adjusted_width

#excelファイルを保存する
wb1.save(inputfile)