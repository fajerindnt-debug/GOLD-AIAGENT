import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Gold AI Agent",
    page_icon="📈",
    layout="wide"
)

# Demo dashboard - belum memakai data pasar real-time
st.title("1817712cb3484fe1ad458ee262603697")
st.caption("QUANT RESEARCH | TEST MODE | SIGNAL ONLY")

# Buat data candle simulasi
rng = np.random.default_rng(42)
n = 100
dates = pd.date_range(
    end=pd.Timestamp.now().floor("min"),
    periods=n,
    freq="min"
)

close = 4000 + np.cumsum(rng.normal(0, 2, n))
open_ = np.r_[close[0], close[:-1]]
high = np.maximum(open_, close) + rng.uniform(0.2, 2, n)
low = np.minimum(open_, close) - rng.uniform(0.2, 2, n)

df = pd.DataFrame({
    "Time": dates,
    "Open": open_,
    "High": high,
    "Low": low,
    "Close": close
})

# Ringkasan
c1, c2, c3, c4 = st.columns(4)
c1.metric("SYMBOL", "XAU/USD")
c2.metric("LAST PRICE", f"{close[-1]:.2f}")
c3.metric("TIMEFRAME", "M1 DEMO")
c4.metric("TRADING MODE", "SIGNAL ONLY")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Grafik",
    "🧮 Quant",
    "🔬 Research",
    "📈 Performance",
    "🎯 Signal"
])

with tab1:
    st.subheader("Candlestick Chart")
    fig = go.Figure(data=[go.Candlestick(
        x=df["Time"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Demo XAU/USD"
    )])
    fig.update_layout(
        template="plotly_dark",
        height=480,
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=20, b=10)
    )
    st.plotly_chart(
        fig, use_container_width=True
    )
    st.caption(
        "Harga simulasi, bukan harga pasar."
    )

with tab2:
    st.subheader("Quant Overview")
    returns = pd.Series(close).pct_change().dropna()
    st.metric("Momentum 10 candle",
              f"{close[-1] - close[-11]:.2f}")
    st.metric("Volatilitas return",
              f"{returns.std() * 100:.4f}%")
    st.write("Data ini hanya untuk menguji tampilan.")

with tab3:
    st.subheader("Research Lab")
    st.write("Modul pengujian strategi")
    st.info("Belum ada hasil backtest nyata.")
    st.write("Nanti: factor analysis, walk-forward, OOS.")

with tab4:
    st.subheader("Performance")
    a, b, c = st.columns(3)
    a.metric("Win Rate", "Belum tersedia")
    b.metric("Expectancy", "Belum tersedia")
    c.metric("Max Drawdown", "Belum tersedia")
    st.write("Statistik akan diisi dari jurnal transaksi.")

with tab5:
    st.subheader("Signal Center")
    st.warning("MODE DEMO — bukan sinyal trading")
    st.write("BUY / SELL: belum diaktifkan")
    st.write("Entry: —")
    st.write("Stop Loss: —")
    st.write("Take Profit: —")
    st.write("Auto-order: OFF")

    if st.button("TEST DASHBOARD"):
        st.success("Tombol berfungsi! Dashboard berjalan.")

st.divider()
st.caption(
    "Gold AI Agent | Prototype v0.1 | Signal-only"
)
