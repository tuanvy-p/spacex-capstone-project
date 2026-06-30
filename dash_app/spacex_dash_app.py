"""
SpaceX Falcon 9 Launch Records Dashboard
Coursera / IBM Data Science Capstone Project

Run:
    python spacex_dash_app.py

Then open the local URL shown in the terminal, usually:
    http://127.0.0.1:8050/
"""

import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATHS = [
    os.path.join(BASE_DIR, "..", "data", "spacex_cleaned_data.csv"),
    os.path.join(BASE_DIR, "..", "data", "spacex_cleaned_sample.csv"),
    os.path.join(BASE_DIR, "..", "data", "spacex_api_raw.csv"),
]


def load_data() -> pd.DataFrame:
    """Load project data with a small fallback dataset for portability."""
    for path in DATA_PATHS:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
    else:
        df = pd.DataFrame({
            "FlightNumber": list(range(1, 11)),
            "PayloadMass": [6104, 525, 677, 500, 3170, 3325, 2296, 1316, 4535, 9600],
            "LaunchSite": [
                "CCSFS SLC 40", "CCSFS SLC 40", "VAFB SLC 4E", "KSC LC 39A",
                "CCSFS SLC 40", "KSC LC 39A", "VAFB SLC 4E", "CCSFS SLC 40",
                "KSC LC 39A", "CCSFS SLC 40",
            ],
            "Orbit": ["LEO", "ISS", "PO", "GTO", "LEO", "ISS", "GTO", "SSO", "LEO", "GTO"],
            "Class": [0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
        })

    # Standardize common column names used across the Coursera labs.
    if "Payload Mass (kg)" in df.columns and "PayloadMass" not in df.columns:
        df = df.rename(columns={"Payload Mass (kg)": "PayloadMass"})
    if "Launch Site" in df.columns and "LaunchSite" not in df.columns:
        df = df.rename(columns={"Launch Site": "LaunchSite"})
    if "Outcome" in df.columns and "Class" not in df.columns:
        df["Class"] = df["Outcome"].astype(str).str.lower().isin(["true", "1", "success", "successful"]).astype(int)

    required_defaults = {
        "PayloadMass": 0,
        "LaunchSite": "Unknown",
        "Orbit": "Unknown",
        "Class": 0,
    }
    for col, default in required_defaults.items():
        if col not in df.columns:
            df[col] = default

    df["PayloadMass"] = pd.to_numeric(df["PayloadMass"], errors="coerce").fillna(df["PayloadMass"].median())
    df["Class"] = pd.to_numeric(df["Class"], errors="coerce").fillna(0).astype(int)
    df["LaunchSite"] = df["LaunchSite"].fillna("Unknown")
    df["Orbit"] = df["Orbit"].fillna("Unknown")
    return df


spacex_df = load_data()
launch_sites = sorted(spacex_df["LaunchSite"].dropna().unique())
site_options = [{"label": "All Sites", "value": "ALL"}] + [
    {"label": site, "value": site} for site in launch_sites
]

min_payload = float(spacex_df["PayloadMass"].min())
max_payload = float(spacex_df["PayloadMass"].max())

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={"fontFamily": "Arial", "margin": "32px"},
    children=[
        html.H1("SpaceX Falcon 9 Launch Records Dashboard", style={"textAlign": "center"}),
        html.P(
            "Interactive visual analytics for launch-site success rates and payload mass versus launch outcome.",
            style={"textAlign": "center"},
        ),

        html.Label("Select Launch Site:"),
        dcc.Dropdown(
            id="site-dropdown",
            options=site_options,
            value="ALL",
            clearable=False,
            style={"marginBottom": "24px"},
        ),

        html.Label("Select Payload Range (kg):"),
        dcc.RangeSlider(
            id="payload-slider",
            min=min_payload,
            max=max_payload,
            step=100,
            value=[min_payload, max_payload],
            marks={
                int(min_payload): str(int(min_payload)),
                int(max_payload): str(int(max_payload)),
            },
            tooltip={"placement": "bottom", "always_visible": False},
        ),

        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "24px", "marginTop": "32px"},
            children=[
                dcc.Graph(id="success-pie-chart"),
                dcc.Graph(id="payload-scatter-chart"),
            ],
        ),
    ],
)


@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value"),
)
def update_pie(selected_site):
    if selected_site == "ALL":
        pie_df = spacex_df.groupby("LaunchSite", as_index=False)["Class"].mean()
        pie_df["SuccessRate"] = pie_df["Class"]
        fig = px.pie(
            pie_df,
            values="SuccessRate",
            names="LaunchSite",
            title="Total Success Rate by Launch Site",
        )
    else:
        filtered = spacex_df[spacex_df["LaunchSite"] == selected_site].copy()
        filtered["OutcomeLabel"] = filtered["Class"].map({1: "Successful Landing", 0: "Failed Landing"})
        outcome_counts = filtered["OutcomeLabel"].value_counts().reset_index()
        outcome_counts.columns = ["Outcome", "Count"]
        fig = px.pie(
            outcome_counts,
            values="Count",
            names="Outcome",
            title=f"Landing Outcome Distribution for {selected_site}",
        )
    return fig


@app.callback(
    Output("payload-scatter-chart", "figure"),
    Input("site-dropdown", "value"),
    Input("payload-slider", "value"),
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    filtered = spacex_df[(spacex_df["PayloadMass"] >= low) & (spacex_df["PayloadMass"] <= high)].copy()
    if selected_site != "ALL":
        filtered = filtered[filtered["LaunchSite"] == selected_site]

    filtered["OutcomeLabel"] = filtered["Class"].map({1: "Successful", 0: "Failed"})
    fig = px.scatter(
        filtered,
        x="PayloadMass",
        y="Class",
        color="OutcomeLabel",
        hover_data=["LaunchSite", "Orbit"],
        title="Payload Mass vs Launch Outcome",
        labels={"PayloadMass": "Payload Mass (kg)", "Class": "Landing Outcome"},
    )
    fig.update_yaxes(tickmode="array", tickvals=[0, 1], ticktext=["Failed", "Success"])
    return fig


if __name__ == "__main__":
    app.run(debug=True)
