import csv
import datetime
import time
from datetime import timedelta

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag


def main():
    base_url: str = "https://fx.minkabu.jp"
    str_now_time = (datetime.datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    start_url: str = base_url + "/indicators?date=" + str_now_time
    # start_url: str = base_url + "/indicators?date=2022-01-27"
    next_url = start_url

    data: list = []

    while True:
        str_url_date = next_url.split("=")[1]
        url_date: datetime.datetime = datetime.datetime.strptime(
            str_url_date, "%Y-%m-%d"
        )
        if (datetime.datetime.now() - url_date).days < -60:
            break
        html = requests.get(next_url)

        soup: BeautifulSoup = BeautifulSoup(html.text, "lxml")
        next_tag = soup.find("a", attrs={"title": "次の週"})
        if type(next_tag) is Tag:
            next_url = base_url + str(next_tag.get("href"))

        index_tabales: ResultSet[Tag] = get_index_table(soup)

        for table in index_tabales:
            caption = table.find("caption")
            if caption is not None:
                # 日付の取得
                year: int = int(caption.text[0:4])
                month: int = int(caption.text[5:7])
                date: int = int(caption.text[8:10])
                rows: ResultSet[Tag] = table.find_all("tr")
                for row in rows:
                    columns: ResultSet[Tag] = row.find_all("td")
                    imgs: ResultSet[Tag] = columns[2].find_all(
                        "img", attrs={"alt": "Star fill"}
                    )
                    rank = len(imgs)  # 重要度
                    if rank == 0:
                        continue
                    index_column_text = columns[1].find("p")
                    index_name: str = ""
                    if index_column_text is not None:
                        index_name = index_column_text.text
                    split_str = index_name.split("・")
                    country = split_str[0]  # 国
                    # 時刻
                    tstr: str = columns[0].text.strip()
                    hour: int = int(tstr[0:2])
                    minute: int = int(tstr[3:5])
                    tdatetime = datetime.datetime(year, month, date, hour, minute)
                    data.append(
                        [
                            tdatetime.strftime("%Y.%m.%d %H:%M:%S"),
                            country,
                            index_name,
                            rank,
                        ]
                    )
        time.sleep(5)
    with open("latest_calendar.csv", "w", newline="", encoding="shift-jis") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(data)


def get_index_table(soup: BeautifulSoup) -> ResultSet[Tag]:
    index_table: ResultSet[Tag] = soup.find_all("table", class_="tbl-border")
    return index_table


if __name__ == "__main__":
    main()
