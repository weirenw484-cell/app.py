import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# ======================
# 頁面設定
# ======================

st.set_page_config(
    page_title="AI 股票助手",
    layout="wide"
)

st.title("📈 AI 股票助手 Dashboard")

# ======================
# 讀取持股
# ======================

df = pd.read_csv("portfolio.csv")

# ======================
# 計算資料
# ======================

current_prices = []
profits = []
market_values = []

for index, row in df.iterrows():

    stock = row["stock"]

    shares = row["shares"]

    cost = row["cost"]

    try:

        ticker = yf.Ticker(stock)

        hist = ticker.history(period="1d")

        current_price = round(hist["Close"].iloc[-1], 2)

    except:

        current_price = 0

    profit = round(
        (current_price - cost) * shares,
        2
    )

    market_value = round(
        current_price * shares,
        2
    )

    current_prices.append(current_price)

    profits.append(profit)

    market_values.append(market_value)

df["現價"] = current_prices
df["損益"] = profits
df["市值"] = market_values

# ======================
# KPI
# ======================

total_profit = sum(profits)
total_value = sum(market_values)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "💰 總資產",
        f"${total_value:,.0f}"
    )

with col2:

    st.metric(
        "📈 總損益",
        f"${total_profit:,.0f}"
    )

# ======================
# 持股表
# ======================

st.header("📊 我的持股")

st.dataframe(
    df,
    use_container_width=True
)

# ======================
# 圓餅圖
# ======================

st.header("📌 持股配置")

fig = px.pie(
    df,
    names="name",
    values="市值",
    title="持股市值分布"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ======================
# 美股資訊
# ======================

st.header("🇺🇸 美股狀況")

indices = {
    "Nasdaq": "^IXIC",
    "S&P500": "^GSPC",
    "NVIDIA": "NVDA"
}

cols = st.columns(3)

i = 0

for name, ticker_symbol in indices.items():

    ticker = yf.Ticker(ticker_symbol)

    hist = ticker.history(period="2d")

    change = (
        (hist["Close"].iloc[-1] - hist["Close"].iloc[-2])
        / hist["Close"].iloc[-2]
    ) * 100

    cols[i].metric(
        name,
        f"{change:.2f}%"
    )

    i += 1

# ======================
# 新增持股
# ======================

st.header("➕ 新增持股")

with st.form("add_stock"):

    stock = st.text_input("股票代號")

    name = st.text_input("股票名稱")

    shares = st.number_input(
        "股數",
        min_value=1
    )

    cost = st.number_input(
        "成本價",
        min_value=0.0
    )

    submit = st.form_submit_button("新增")

    if submit:

        new_data = pd.DataFrame([{
            "stock": stock,
            "name": name,
            "shares": shares,
            "cost": cost
        }])

        df = pd.concat(
            [df, new_data],
            ignore_index=True
        )

        df.to_csv(
            "portfolio.csv",
            index=False
        )

        st.success("新增成功！")

# ======================
# 刪除持股
# ======================

st.header("❌ 刪除持股")

delete_stock = st.selectbox(
    "選擇股票",
    df["stock"]
)

if st.button("刪除"):

    df = df[df["stock"] != delete_stock]

    df.to_csv(
        "portfolio.csv",
        index=False
    )

    st.success("刪除成功！")
