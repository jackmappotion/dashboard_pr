import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input
from controller import Controller

raw_df = pd.read_csv("./data/data.csv", encoding="cp949")
controller = Controller(raw_df)
app = Dash(__name__)

##
# line_numbers = sorted(set(raw_df["호선"]))


app.layout = html.Div(
    [
        html.H1("지하철 혼잡도", style={"textAlign": "center"}),
        dcc.Dropdown(
            id="first-dropdown",
            options=[
                {"label": f"{line_number} 호선", "value": line_number}
                for line_number in sorted(set(raw_df["호선"]))
            ],
        ),
        html.Br(),
        dcc.Dropdown(id="second-dropdown"),
        html.Br(),
        dcc.Dropdown(
            id="third-dropdown",
            options=[
                {"label": "상선", "value": "상선"},
                {"label": "하선", "value": "하선"},
            ],
        ),
        html.Br(),
        dcc.Dropdown(
            id="fourth-dropdown",
            options=[
                {"label": "평일", "value": "평일"},
                {"label": "토요일", "value": "토요일"},
                {"label": "일요일", "value": "일요일"},
            ],
        ),
        html.Div(id="display-container"),
    ]
)


@app.callback(
    Output("second-dropdown", "options"),
    Input("first-dropdown", "value"),
)
def set_options(line_number):
    station_names = sorted(
        set(raw_df[raw_df["호선"] == line_number]["출발역"])
    )
    station_name_dict = [
        {"label": station_name, "value": station_name}
        for station_name in station_names
    ]
    return station_name_dict


@app.callback(
    Output("display-container", "children"),
    [
        Input("first-dropdown", "value"),
        Input("second-dropdown", "value"),
        Input("third-dropdown", "value"),
        Input("fourth-dropdown", "value"),
    ],
)
def draw_graph(line_number, station_name, way, weekday_type):
    if None in [line_number, station_name, way, weekday_type]:

        return html.Div(
            "Please make sure all selections are made to display the heatmap."
        )
    final_df = controller(line_number, station_name, way, weekday_type)
    fig = px.imshow(
        final_df,
        labels=dict(x="Time", y="Station", color="Congestion"),
        x=final_df.columns,
        y=final_df.index,
        aspect="auto",
        color_continuous_scale="OrRd",
        zmin=0,
        zmax=100,
    )

    fig.update_layout(
        title_text="Subway Station Congestion Heatmap",
        title_x=0.5,
        xaxis_title="Station",
        yaxis_title="Time",
        coloraxis_colorbar=dict(title="Congestion Level"),
    )

    # Return the dcc.Graph component with the figure
    return dcc.Graph(figure=fig)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
