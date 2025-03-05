import os
import dash
from dash import Dash, html, dcc, Output, Input, State
from dash.exceptions import PreventUpdate

from functions.create_database import create_centralized_db




app = Dash(__name__, use_pages=True, meta_tags=[{"name": "viewport", "content": "width=device-width"} ] ,suppress_callback_exceptions=True)



server = app.server

# url_base_pathname="/Lutur_Data_App/"
app.title = "InWave"
app._favicon = "favicon.ico"


app.layout = html.Div(
    [
        # dcc.Store(id="store", data={}),
        dcc.Store(id='store', storage_type='session'),
        # dcc.Location(id='url', refresh=False),
        html.Div(id='content'),
        # html.H1("Multi Page App Demo: Sharing data between pages"),

        ####################### visualize menu

        dash.page_container,
    ]
)



if __name__ == '__main__':
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/asset/json_credentials.json"
    app.run_server(host='0.0.0.0', port=8050, debug=True, use_reloader=False)



