import pandas as pd

# 讀取你剛剛的資料
df = pd.read_csv("stock_app_reviews.csv")

# ===== 情感分析 =====
def sentiment(score):
    if score >= 4:
        return "正評"
    elif score == 3:
        return "中立"
    else:
        return "負評"

df["sentiment"] = df["score"].apply(sentiment)

# ===== UI分類 =====
def classify_ui(text):
    text = str(text)

    if any(k in text for k in ["卡", "慢", "當機", "lag"]):
        return "操作流暢性"
    elif any(k in text for k in ["不好用", "複雜", "找不到", "不直覺"]):
        return "介面易用性"
    elif any(k in text for k in ["字", "排版", "顏色", "畫面"]):
        return "視覺設計"
    elif any(k in text for k in ["登入", "錯誤", "bug", "失敗"]):
        return "功能問題"
    elif any(k in text for k in ["好用", "方便", "快速", "穩定"]):
        return "正向體驗"
    else:
        return "其他"

df["ui_type"] = df["content"].apply(classify_ui)

# ===== 統計 =====
print("情感分析：")
print(df["sentiment"].value_counts())

print("\nUI分類：")
print(df["ui_type"].value_counts())

# ===== 存新檔案 =====
df.to_csv("analysis_result.csv", index=False, encoding='utf-8-sig')

print("\n完成！已輸出 analysis_result.csv")