from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# ---------- Load & prepare data ----------
DATA_PATH = Path("data") / "formatted_output.csv"
df = pd.read_csv(DATA_PATH)

# Normalize columns / types
df["date"] = pd.to_datetime(df["date"])
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# Normalize region strings just in case (e.g., "North" -> "north")
df["region"] = df["region"].astype(str).str.strip().str.lower()

PRICE_INCREASE_date = pd.to_datetime("2021-01-15")


def build_figure(filtered_df: pd.DataFrame):
    # Aggregate to daily total sales (for a clean line chart)
    daily_sales = (
        filtered_df.groupby("date", as_index=False)["sales"]
        .sum()
        .sort_values("date")
    )

    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        labels={"date": "date", "sales": "sales ($)"},
    )

    # Vertical line marking price increase date (no auto annotation to avoid plotly/pandas Timestamp issue)
    fig.add_vline(x=PRICE_INCREASE_date, line_width=2, line_dash="dash")

    # Add label safely using annotation in paper coords
    fig.add_annotation(
        x=PRICE_INCREASE_date,
        y=1,
        xref="x",
        yref="paper",
        text="Price increase (15 Jan 2021)",
        showarrow=False,
        xanchor="left",
        yanchor="bottom",
        font=dict(size=12),
    )

    fig.update_layout(
        margin=dict(l=40, r=20, t=40, b=40),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.08)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.08)"),
    )

    return fig


# ---------- Dash app ----------
app = Dash(__name__)
app.title = "Pink Morsel sales Visualiser"

# Simple inline "CSS" styling via Dash style dictionaries
styles = {
    "page": {
        "minHeight": "100vh",
        "background": "linear-gradient(180deg, #f6f7fb 0%, #ffffff 60%)",
        "padding": "32px 16px",
        "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif",
        "color": "#1f2937",
    },
    "container": {
        "maxWidth": "1100px",
        "margin": "0 auto",
    },
    "card": {
        "backgroundColor": "white",
        "border": "1px solid rgba(0,0,0,0.08)",
        "borderRadius": "16px",
        "boxShadow": "0 10px 30px rgba(0,0,0,0.06)",
        "padding": "20px",
    },
    "title": {
        "fontSize": "28px",
        "margin": "0 0 8px 0",
        "fontWeight": "750",
        "letterSpacing": "-0.3px",
    },
    "subtitle": {
        "margin": "0 0 16px 0",
        "fontSize": "14px",
        "lineHeight": "1.5",
        "color": "#4b5563",
    },
    "controlsRow": {
        "display": "flex",
        "gap": "16px",
        "alignItems": "center",
        "flexWrap": "wrap",
        "marginBottom": "16px",
    },
    "controlLabel": {
        "fontSize": "13px",
        "fontWeight": "700",
        "color": "#374151",
        "marginBottom": "6px",
    },
    "controlBox": {
        "padding": "12px 14px",
        "borderRadius": "12px",
        "border": "1px solid rgba(0,0,0,0.08)",
        "backgroundColor": "#fafafa",
    },
}

app.layout = html.Div(
    style=styles["page"],
    children=[
        html.Div(
            style=styles["container"],
            children=[
                html.Div(
                    style=styles["card"],
                    children=[
                        html.H1("Soul Foods — Pink Morsel sales Visualiser", style=styles["title"]),
                        html.P(
                            "Use the region filter to explore sales patterns. "
                            "The dashed line marks the Pink Morsel price increase on 15 Jan 2021.",
                            style=styles["subtitle"],
                        ),

                        html.Div(
                            style=styles["controlsRow"],
                            children=[
                                html.Div(
                                    style=styles["controlBox"],
                                    children=[
                                        html.Div("Filter by region", style=styles["controlLabel"]),
                                        dcc.RadioItems(
                                            id="region-radio",
                                            options=[
                                                {"label": "All", "value": "all"},
                                                {"label": "North", "value": "north"},
                                                {"label": "East", "value": "east"},
                                                {"label": "South", "value": "south"},
                                                {"label": "West", "value": "west"},
                                            ],
                                            value="all",
                                            inline=True,
                                            style={"fontSize": "14px"},
                                            inputStyle={"marginRight": "6px", "marginLeft": "12px"},
                                        ),
                                    ],
                                ),
                            ],
                        ),

                        dcc.Graph(
                            id="sales-line-chart",
                            figure=build_figure(df),
                            config={"displayModeBar": True},
                            style={"height": "520px"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# ---------- Callback ----------
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-radio", "value"),
)
def update_chart(selected_region: str):
    if selected_region == "all":
        filtered = df
    else:
        filtered = df[df["region"] == selected_region]

    return build_figure(filtered)


if __name__ == "__main__":
    app.run(debug=True)