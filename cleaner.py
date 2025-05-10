import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('sp500_data.csv')

# Seleccionar solo las columnas que te interesan
df_cleaned = df[['Date', 'Open', 'Close']]

# Guardar el DataFrame limpio a un nuevo archivo CSV (opcional)
df_cleaned.to_csv('Prices.csv', index=False)

# Mostrar las primeras filas para verificar
print(df_cleaned.head())
