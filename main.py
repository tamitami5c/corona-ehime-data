import json
import csv
import datetime

import requests
from util import download_file


def main():
    #愛媛県のopendata
    url="https://www.pref.ehime.jp/opendata-catalog/dataset/2174/resource/7072/380008_ehime_covid19_patients.csv"
    file_name=download_file(url)
    #日付とその日の陽性者数をセットしていく
    data={}
    with open(file_name,encoding="utf-8") as f:
        reader=csv.reader(f)
        _=next(reader) #headerは飛ばす
        
        for  row in reader:
            date=row[4] #これってisoformat?
            if date in data:
                data[date]+=1
            else:
                data[date]=1

    #json形式にするためにフォーマット整える
    #初めて陽性者が確認された日から後の日付で、陽性者が確認されていない日は 0を記入する。
    date_list=sorted(data.keys(),key=lambda x: datetime.date.fromisoformat(x))
    first_date=datetime.date.fromisoformat(date_list[0])
    last_date=datetime.date.fromisoformat(date_list[-1])
    print("日付(最初):",first_date)
    print("日付(最後):",last_date)

    def daterange(start_date,end_date):
        """
        start_date(含む)からend_date(含む)まで
        """
        for n in range(int((end_date-start_date).days)+1):
            yield start_date+datetime.timedelta(n)
    result=[]
    for d in daterange(first_date,last_date):
        date=d.isoformat()
        count=data[date] if  (date in data) else 0
        item={
            "date":date,
            "count":count
        }
        result.append(item)

    #jsonに書きだし
    data={
        "data":result
    }
    print(data)

    with open("ehime_data.json","w") as f:
        json.dump(data,f,indent=4)

if __name__ == "__main__":
    main()
