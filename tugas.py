# =====================================
# DASHBOARD VAKSINASI COVID-19
# Dibuat dengan Streamlit
# =====================================

import streamlit as st
import pandas as pd
import altair as alt

# -------------------------------------
# KONFIGURASI HALAMAN
# -------------------------------------
st.set_page_config(
    page_title="Dashboard Vaksinasi COVID-19",
    page_icon="💉",
    layout="wide"
)

# -------------------------------------
# LOAD DATA
# -------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("country_vaccinations.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# -------------------------------------
# SIDEBAR FILTER
# -------------------------------------
st.sidebar.markdown("## 🔍 Filter Data")
st.sidebar.caption("Gunakan filter untuk eksplorasi data")

negara = st.sidebar.multiselect(
    "🌍 Pilih Negara",
    options=sorted(df["country"].dropna().unique()),
    default=["Indonesia"] if "Indonesia" in df["country"].values else []
)

tanggal = st.sidebar.date_input(
    "📅 Rentang Tanggal",
    [df["date"].min(), df["date"].max()]
)

# -------------------------------------
# FILTER DATA
# -------------------------------------
df_view = df.copy()

if negara:
    df_view = df_view[df_view["country"].isin(negara)]

df_view = df_view[
    (df_view["date"] >= pd.to_datetime(tanggal[0])) &
    (df_view["date"] <= pd.to_datetime(tanggal[1]))
]

# -------------------------------------
# HEADER
# -------------------------------------
st.title("💉 Dashboard Vaksinasi COVID-19")
st.caption("Visualisasi interaktif perkembangan vaksinasi COVID-19 per negara")

st.divider()

# -------------------------------------
# KPI
# -------------------------------------
c1, c2, c3 = st.columns(3)

c1.metric("🌍 Jumlah Negara", df_view["country"].nunique())
c2.metric("💉 Total Vaksinasi (Maks)", f"{int(df_view['total_vaccinations'].max() or 0):,}")
c3.metric("✅ Fully Vaccinated (Maks)", f"{int(df_view['people_fully_vaccinated'].max() or 0):,}")

st.divider()

# -------------------------------------
# GRAFIK
# -------------------------------------
st.subheader("📈 Tren Total Vaksinasi")
st.caption("Akumulasi total vaksinasi dari waktu ke waktu")

grafik_df = (
    df_view
    .dropna(subset=["total_vaccinations"])
    .groupby("date", as_index=False)["total_vaccinations"]
    .sum()
)

chart = alt.Chart(grafik_df).mark_line(
    color="#1565C0",
    strokeWidth=3
).encode(
    x=alt.X("date:T", title="Tanggal"),
    y=alt.Y("total_vaccinations:Q", title="Total Vaksinasi"),
    tooltip=["date:T", "total_vaccinations:Q"]
).properties(height=420)

st.altair_chart(chart, use_container_width=True)

st.divider()

# -------------------------------------
# TABEL
# -------------------------------------
st.subheader("📋 Tabel Data Vaksinasi")
st.caption("Data detail sesuai filter yang dipilih")

st.dataframe(
    df_view.sort_values("date", ascending=False),
    use_container_width=True,
    hide_index=True
)

# -------------------------------------
# FOOTER
# -------------------------------------
st.caption("📁 Sumber Data: country_vaccinations.csv | Dibuat dengan Streamlit")
