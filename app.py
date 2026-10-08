import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Airline Passenger Time Series")

@st.cache_data
def load_data():
    df = pd.read_csv("AirPassengers.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")

df = load_data()

st.write(
    "This dataset shows monthly international airline passenger totals "
    "from 1949 to 1960, measured in thousands of passengers."
)

st.sidebar.header("Options")

resolution = st.sidebar.selectbox(
    "Select time resolution", ["Monthly", "Quarterly"]
)

show_rolling = st.sidebar.checkbox(
    "Show rolling statistics", value=True
)

if resolution == "Monthly":
    data = df.resample("MS").mean()
    window = 12
else:
    data = df.resample("QS").mean()
    window = 4

rolling_mean = data["value"].rolling(window).mean()
rolling_std = data["value"].rolling(window).std()

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()

    ax.plot(data.index, data["value"], label="Passengers")

    if show_rolling:
        ax.plot(data.index, rolling_mean, label="Rolling mean")
        ax.fill_between(
            data.index,
            rolling_mean - 2 * rolling_std,
            rolling_mean + 2 * rolling_std,
            alpha=0.2,
            label="±2 rolling SD"
        )

    ax.set_xlabel("Date")
    ax.set_ylabel("Passengers (thousands)")
    ax.set_title(f"Airline Passengers: {resolution} Resolution")
    ax.set_ylim(bottom=0)
    ax.legend()

    st.pyplot(fig)

with col2:
    st.subheader("Seasonality")

    seasonal = df.copy()
    seasonal["month"] = seasonal.index.month
    seasonal_pattern = seasonal.groupby("month")["value"].mean()

    fig, ax = plt.subplots()

    ax.plot(
        seasonal_pattern.index,
        seasonal_pattern.values,
        marker="o"
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Average passengers (thousands)")
    ax.set_title("Average Passenger Volume by Month")
    ax.set_xticks(range(1, 13))

    st.pyplot(fig)

st.subheader("Interpretation")

st.write(
    "The time series shows a clear upward trend in airline passenger volume "
    "from 1949 through 1960. Passenger levels also follow a repeating yearly "
    "pattern, with higher values during the middle of the year and lower "
    "values during the beginning and end of the year. This indicates a strong "
    "seasonal component in the data."
)

st.write(
    "The rolling mean helps show the overall trend by smoothing short-term "
    "changes. The shaded region represents plus or minus two rolling standard "
    "deviations around the rolling mean. This band shows how much the observed "
    "values vary over time and should not be interpreted as a formal confidence "
    "interval."
)

st.subheader("Temporal Honesty")

st.write(
    "The y-axis begins at zero so that changes in passenger volume are not "
    "visually exaggerated. Monthly resolution preserves the yearly seasonal "
    "pattern, while quarterly resolution provides a smoother view of the "
    "long-term trend. Using both resolutions makes it possible to examine the "
    "data at different levels of temporal detail."
)
