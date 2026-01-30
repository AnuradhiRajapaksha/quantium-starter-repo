from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

#load data
data_path= Path("data")/"formatted_output.csv"
df= pd.read_csv(data_path)

#ensure correct type
df["date"]=pd.to_datetime(df["date"])
df["sales"]=pd.to_numeric(df["sales"],errors="coerce")

#aggregate to total sales per day (acress regions)
daily_sales=(
    df.groupby("date",as_index=False)["sales"]
    .sum()
    .sort_values("date")
)

#price increase date
increase_date=pd.to_datetime("2021-01-15")

#figure
fig=px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Total Pink Morsels Sales Over Time",
    labels={"date":"Date", "sales":"Sales($)"},
)

#add a vertical line to mark price increase date
fig.add_vline(
    x=increase_date,
    line_width=2,
    line_dash="dash",
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales ($)",
)

##---Dash App---##
app=Dash(__name__)

app.layout=html.Div(
    style={"maxWidth":"1100px", "margin":"40px auto","fontFamily":"Arial"},
    children=[
        html.H1("Soul Foods-Pink Morsels Sales Visualiser"),
        html.P("Question : Were sales higher before or after the price increase?"),
        dcc.Graph(figure=fig),
    ]
)


if __name__=="__main__":
    app.run(debug=True) 