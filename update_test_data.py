import csv
import json
import datetime
from util import download_file


def fetch_and_save_test_data():
    url="https://www.pref.ehime.jp/opendata-catalog/dataset/2174/resource/7073/380008_ehime_covid19_test_people.csv"
    file_name=download_file(url)

    d=[]
    with open(file_name,encoding="utf-8") as f:
        reader=csv.reader(f)
        _=next(reader) #headerは飛ばす
        
        for  row in reader:
            date=row[0]
            num_tests=row[4]

            d.append({
                "実施_年月日":date,
                "検査実施_人数":num_tests
            })

    print(d)
    jst = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    last_updated=datetime.datetime.now(jst)
    data={
        "last_updated":last_updated.isoformat(),
        "data":d
    }
    with open("test_data.json","w") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)


if __name__=="__main__":
    fetch_and_save_test_data()