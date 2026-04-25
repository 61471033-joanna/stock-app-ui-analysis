import pandas as pd
from collections import Counter
import re

# ===== 1. 讀取三家資料 =====
fubon = pd.read_csv("fubon_big.csv")
cathay = pd.read_csv("cathay_reviews.csv")
kgi = pd.read_csv("kgi_reviews.csv")

# ===== 2. 加上公司名稱 =====
fubon["company"] = "富邦"
cathay["company"] = "國泰"
kgi["company"] = "凱基"

# ===== 3. 合併資料 =====
df = pd.concat([fubon, cathay, kgi], ignore_index=True)

# ===== 4. 基本清理 =====
df["content"] = df["content"].astype(str)
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df = df.dropna(subset=["score", "content"])

# ===== 5. 情緒分析 =====
def sentiment(score):
    if score >= 4:
        return "正評"
    elif score == 3:
        return "中立"
    else:
        return "負評"

df["sentiment"] = df["score"].apply(sentiment)

# ===== 6. UI 問題大分類 =====
def classify_ui(text):
    text = str(text)

    # 視覺設計：放前面，避免被其他類別吃掉
    if any(k in text for k in [
        "字", "字體", "字太小", "字太大",
        "排版", "版面", "畫面", "介面",
        "顏色", "配色", "設計", "醜", "美觀",
        "圖示", "icon", "按鈕", "閱讀",
        "看不清楚", "不好看", "清楚", "清晰"
    ]):
        return "視覺設計"

    elif any(k in text for k in ["卡", "慢", "當機", "lag", "閃退"]):
        return "操作流暢性"

    elif any(k in text for k in ["不好用", "複雜", "找不到", "不直覺"]):
        return "介面易用性"

    elif any(k in text for k in ["登入", "錯誤", "bug", "失敗", "憑證"]):
        return "功能問題"

    elif any(k in text for k in ["好用", "方便", "快速", "穩定"]):
        return "正向回饋"

    else:
        return "其他"

df["ui_type"] = df["content"].apply(classify_ui)

# ===== 7. 視覺設計細分類 =====
def classify_visual(text):
    text = str(text)

    if any(k in text for k in ["字", "字體", "字太小", "字太大", "文字", "閱讀", "看不清楚"]):
        return "字體與可讀性"

    elif any(k in text for k in ["排版", "版面", "畫面", "資訊太多", "雜亂", "清楚", "清晰"]):
        return "版面配置"

    elif any(k in text for k in ["顏色", "配色", "色彩", "亮", "暗"]):
        return "色彩與配色"

    elif any(k in text for k in ["按鈕", "圖示", "icon", "選單", "位置"]):
        return "按鈕與圖示"

    elif any(k in text for k in ["介面", "設計", "醜", "不好看", "美觀"]):
        return "整體介面設計"

    else:
        return "其他視覺相關"

visual_df = df[df["ui_type"] == "視覺設計"].copy()
visual_df["visual_type"] = visual_df["content"].apply(classify_visual)

# ===== 8. 整體情緒統計 =====
sentiment_table = pd.crosstab(df["company"], df["sentiment"])
print("=== 各券商情緒分析 ===")
print(sentiment_table)

# ===== 9. UI 大分類統計 =====
ui_table = pd.crosstab(df["company"], df["ui_type"])
print("\n=== 各券商 UI 問題分類 ===")
print(ui_table)

# ===== 10. 視覺設計細分類統計 =====
visual_table = pd.crosstab(visual_df["company"], visual_df["visual_type"])
print("\n=== 各券商視覺設計細分類 ===")
print(visual_table)

# ===== 11. 視覺設計評論情緒 =====
visual_sentiment_table = pd.crosstab(visual_df["company"], visual_df["sentiment"])
print("\n=== 視覺設計相關評論情緒 ===")
print(visual_sentiment_table)

# ===== 12. 詞頻分析函式 =====
def word_frequency(data, column="content", top_n=20):
    text = " ".join(data[column].astype(str))
    text = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9\s]", " ", text)

    words = text.split()

    # 簡單排除無研究意義的常見詞
    stopwords = [
        "的", "了", "是", "我", "也", "都", "很", "就", "在", "有",
        "和", "與", "不", "沒", "無", "要", "會", "還", "但", "跟",
        "一個", "使用", "APP", "app"
    ]

    words = [w for w in words if w not in stopwords and len(w) > 1]

    counter = Counter(words)
    return pd.DataFrame(counter.most_common(top_n), columns=["word", "count"])

# ===== 13. 全部評論詞頻 =====
top_words = word_frequency(df, top_n=30)
print("\n=== 全部評論常見詞 ===")
print(top_words)

# ===== 14. 負評詞頻 =====
negative_df = df[df["sentiment"] == "負評"]
top_negative_words = word_frequency(negative_df, top_n=30)
print("\n=== 負評常見詞 ===")
print(top_negative_words)

# ===== 15. 視覺設計詞頻 =====
top_visual_words = word_frequency(visual_df, top_n=30)
print("\n=== 視覺設計相關常見詞 ===")
print(top_visual_words)

# ===== 16. 視覺設計負評詞頻 =====
visual_negative_df = visual_df[visual_df["sentiment"] == "負評"]
top_visual_negative_words = word_frequency(visual_negative_df, top_n=30)
print("\n=== 視覺設計負評常見詞 ===")
print(top_visual_negative_words)

# ===== 17. 輸出檔案 =====
df.to_csv("analysis_result.csv", index=False, encoding="utf-8-sig")
visual_df.to_csv("visual_design_reviews.csv", index=False, encoding="utf-8-sig")

sentiment_table.to_csv("sentiment_by_company.csv", encoding="utf-8-sig")
ui_table.to_csv("ui_type_by_company.csv", encoding="utf-8-sig")
visual_table.to_csv("visual_type_by_company.csv", encoding="utf-8-sig")
visual_sentiment_table.to_csv("visual_sentiment_by_company.csv", encoding="utf-8-sig")

top_words.to_csv("top_words.csv", index=False, encoding="utf-8-sig")
top_negative_words.to_csv("top_negative_words.csv", index=False, encoding="utf-8-sig")
top_visual_words.to_csv("top_visual_words.csv", index=False, encoding="utf-8-sig")
top_visual_negative_words.to_csv("top_visual_negative_words.csv", index=False, encoding="utf-8-sig")

print("\n分析完成！已輸出以下檔案：")
print("1. analysis_result.csv")
print("2. visual_design_reviews.csv")
print("3. sentiment_by_company.csv")
print("4. ui_type_by_company.csv")
print("5. visual_type_by_company.csv")
print("6. visual_sentiment_by_company.csv")
print("7. top_words.csv")
print("8. top_negative_words.csv")
print("9. top_visual_words.csv")
print("10. top_visual_negative_words.csv")