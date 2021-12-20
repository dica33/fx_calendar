import pandas as pd

df = pd.read_csv("latest_calendar.csv", encoding="shift-jis")
df = df[~df.duplicated()]
df.to_csv("latest_calendar.csv", index=False, encoding="shift-jis")
