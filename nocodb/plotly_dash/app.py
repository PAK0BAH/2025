import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Загрузка данных из CSV
csv_file = "nocodedb.csv"
df = pd.read_csv(csv_file)

# Очистка и преобразование данных
numeric_columns = ["Fiyat", "Ekran Boyutu", "Ekran Yenileme HД±zД±"]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=["Fiyat", "Ekran Boyutu"])  # Убираем строки без ключевых данных

# Инициализация Dash
app = dash.Dash(__name__)

# Макет приложения
app.layout = html.Div([
    html.H1("Анализ цен и характеристик устройств"),

    html.Label("Выберите бренд:"),
    dcc.Dropdown(
        id="brand-dropdown",
        options=[{"label": brand, "value": brand} for brand in df["Marka"].unique()],
        value=df["Marka"].unique()[0],
        clearable=False
    ),

    html.Label("Выберите процессор:"),
    dcc.Dropdown(
        id="cpu-dropdown",
        options=[{"label": cpu, "value": cpu} for cpu in df["Д°Еџlemci Tipi"].unique()],
        value=df["Д°Еџlemci Tipi"].unique()[0],
        clearable=False
    ),

    dcc.Graph(id="price-screen-graph")
])


# Callback для обновления графика
@app.callback(
    Output("price-screen-graph", "figure"),
    [Input("brand-dropdown", "value"), Input("cpu-dropdown", "value")]
)
def update_graph(selected_brand, selected_cpu):
    filtered_df = df[(df["Marka"] == selected_brand) & (df["Д°Еџlemci Tipi"] == selected_cpu)]

    fig = px.scatter(
        filtered_df, x="Ekran Boyutu", y="Fiyat",
        color="Ekran KartД±",
        size="Ekran Yenileme HД±zД±",
        hover_data=["Ram (Sistem BelleДџi)", "SSD Kapasitesi"],
        title=f"Цены и характеристики для {selected_brand} с {selected_cpu}"
    )

    return fig


# Запуск приложения
if __name__ == "__main__":
    app.run_server(debug=True)