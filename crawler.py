from google_play_scraper import reviews, Sort
import pandas as pd

app_id = "com.fubon.mbank"

all_data = []
continuation_token = None

while True:
    result, continuation_token = reviews(
        app_id,
        lang='zh_TW',
        country='tw',
        sort=Sort.NEWEST,
        count=200,
        continuation_token=continuation_token
    )

    if not result:
        break

    print(f"抓到 {len(result)} 筆，目前總數：{len(all_data)}")

    for r in result:
        all_data.append({
            "user": r['userName'],
            "score": r['score'],
            "content": r['content'],
            "date": r['at']
        })

    if continuation_token is None:
        break

df = pd.DataFrame(all_data)
df.to_csv("fubon_big.csv", index=False, encoding='utf-8-sig')

print("完成！")