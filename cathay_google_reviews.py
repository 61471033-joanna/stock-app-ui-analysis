from google_play_scraper import reviews, Sort
import pandas as pd

app_id = "com.cathaysec.eservice"

all_data = []
continuation_token = None

while True:
    result, continuation_token = reviews(
        app_id,
        lang="zh_TW",
        country="tw",
        sort=Sort.NEWEST,
        count=200,
        continuation_token=continuation_token
    )

    if not result:
        print("沒有抓到資料，請確認 app_id")
        break

    print(f"抓到 {len(result)} 筆，目前總數：{len(all_data) + len(result)}")

    for r in result:
        all_data.append({
            "company": "國泰證券",
            "user": r.get("userName", ""),
            "score": r.get("score", ""),
            "content": r.get("content", ""),
            "date": r.get("at", "")
        })

    if continuation_token is None:
        break

df = pd.DataFrame(all_data)
df.to_csv("cathay_reviews.csv", index=False, encoding="utf-8-sig")

print(f"完成！共 {len(df)} 筆，已存成 cathay_reviews.csv")