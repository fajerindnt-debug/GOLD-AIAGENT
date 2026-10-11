
import os
import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Gold AI Agent",
    page_icon="📈",
    layout="wide"
)

st.title("🥇 GOLD AI AGENT")
st.caption("QUANT RESEARCH | TEST MODE | SIGNAL ONLY")

# Baca API key dari Streamlit Secrets
try:
    API_KEY = st.secrets["TWELVE_DATA_API_KEY"]
except Exception:
    API_KEY = os.getenv("TWELVE_DATA_API_KEY", "")


@st.cache_data(ttl=60)
def get_candles(api_key, interval="1min"):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": "XAU/USD",
        "interval": interval,
        "outputsize": 100,
        "apikey": api_key,
        "format": "JSON"
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    result = response.json()

    if "values" not in result:
        raise ValueError(
            result.get("message", "Data candle tidak tersedia")
        )

    df = pd.DataFrame(result["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])

    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.dropna().sort_values("datetime")


if not API_KEY:
    st.warning(
        "API key belum dipasang. Buka Manage app > Settings > Secrets."
    )
else:
    interval = st.selectbox(
        "Timeframe candle",
        ["1min", "5min", "15min", "1h"],
        index=2
    )

    if st.button("🔄 Refresh data"):
        st.cache_data.clear()

    try:
        df = get_candles(API_KEY, interval)

        st.success("Data berhasil diterima dari Twelve Data")
        st.metric(
            "Harga candle terakhir",
            f'{df["close"].iloc[-1]:,.2f}'
        )
        st.caption(
            f'Waktu candle: {df["datetime"].iloc[-1]}'
        )

        fig = go.Figure(data=[
            go.Candlestick(
                x=df["datetime"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="XAU/USD"
            )
        ])

        fig.update_layout(
            title=f"XAU/USD — {interval}",
            xaxis_rangeslider_visible=False,
            height=550
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
