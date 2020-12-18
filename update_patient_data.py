import csv
import json
import datetime
from util import download_file


def fetch_and_save_patient_data():
    #患者の情報
    url="https://www.pref.ehime.jp/opendata-catalog/dataset/2174/resource/7072/380008_ehime_covid19_patients.csv"
    file_name=download_file(url)

    d=[]
    with open(file_name,encoding="utf-8") as f:
        reader=csv.reader(f)
        _=next(reader) #headerは飛ばす
        
        for  row in reader:
            no=int(row[0])
            realease_date=row[4]
            l=row[7]
            age_group=row[8]
            gender=row[9]

            d.append({
                "No":no,
                "公表_年月日":realease_date,
                "患者_居住地":l,
                "患者_年代":age_group,
                "患者_性別":gender,
            })

    print(d)
    jst = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    last_updated=datetime.datetime.now(jst)
    data={
        "last_updated":last_updated.isoformat(),
        "data":d
    }
    with open("patient_data.json","w") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)


if __name__=="__main__":
    fetch_and_save_patient_data()