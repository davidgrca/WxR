import pandas as pd
import matplotlib.pyplot as plt

# Cargar los archivos CSV
prices_df = pd.read_csv("prices.csv")
weather_df = pd.read_csv("weather.csv")

# Convertir a datetime
# Convertir fechas a datetime
prices_df["Date"] = pd.to_datetime(prices_df["Date"])
weather_df["datetime"] = pd.to_datetime(weather_df["datetime"])

# Seleccionar años válidos
valid_years = [2015, 2016, 2017, 2018, 2019, 2022, 2024]

prices_df = prices_df[prices_df["Date"].dt.year.isin(valid_years)]
weather_df = weather_df[weather_df["datetime"].dt.year.isin(valid_years)]


# Calcular retorno diario: Close / Open
prices_df["Return"] = prices_df["Close"] / prices_df["Open"]

# Renombrar columna de fecha en weather para hacer merge
weather_df.rename(columns={"datetime": "Date"}, inplace=True)

# Fusionar por fecha exacta
merged_df = pd.merge(prices_df, weather_df, on="Date", how="inner")


fomc_events = [
    "2015-12-16",  # Primer alza de tasas tras crisis
    "2017-10-04",  # Anuncio de inicio de QT
    "2019-07-31",  # Empieza a bajar tasas (pivote)
    "2020-03-15",  # QE masivo durante COVID
    "2022-03-16",  # Inicio de ciclo de subidas post-COVID
    "2022-06-15",  # QT oficialmente anunciado
]
fomc_dates = pd.to_datetime(fomc_events)


merged_df["Bad_day"] = (
    (merged_df["cloudcover"] > 50) &
    (merged_df["precip"] > 0) &
    (merged_df["feelslike"] < 5)
)

# Gráfico: Retorno diario coloreado por si está nublado
plt.figure(figsize=(14, 6))
plt.scatter(merged_df["Date"], merged_df["Return"], 
            c=merged_df["Bad_day"].map({True: "gray", False: "skyblue"}), 
            label="Retorno diario", alpha=0.7)

for date in fomc_dates:
    plt.axvline(date, color="blue", linestyle=":", linewidth=1.5, label="Evento FOMC")

# Evitar duplicar etiquetas
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

# Títulos y ejes
plt.title("Retorno diario vs Días 'malos' y eventos FOMC (2015–2019)")
plt.xlabel("Fecha")
plt.ylabel("Retorno (Close / Open)")
plt.grid(True)
plt.tight_layout()
plt.show()