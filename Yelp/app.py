import pandas as pd 
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from data.restaurants_dao import get_yelp_dataframe
from dash.dependencies import Input, Output
import flask
from ui.html_components import Components, get_initial_view, ModelCoverter


server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP], server=server, prevent_initial_callbacks=True)

df = get_yelp_dataframe()

model_converter = ModelCoverter(df)
@app.callback(
    Output('cities-dropdown', 'options'),
    Output('geojson', 'data'),
    Output('restaurant_cards', 'children'),
    [Input('states-dropdown', 'value'),
    Input('cities-dropdown', 'value'),
    Input('health-slider', 'value'),
    Input('ratings', 'value'),
    Input('input', 'value')])
def update_text(state_selected,cities_selected,health_score_selected,ratings,search_string):
    filter = {}

    if search_string:
        filter['search_string']=search_string

    if state_selected and state_selected != [''] :
        filter['states_selected'] = state_selected
    
    if cities_selected and cities_selected != ['']:
        filter['cities_selected'] = cities_selected

    filter['health_score_selected'] = health_score_selected
    filter['ratings'] = ratings
    

    df = get_yelp_dataframe(user_selections= filter)
    model_converter = ModelCoverter(df)

    return model_converter.get_unique_cities(), model_converter.get_cluster_makers(), model_converter.get_restaurant_cards()

app.layout = get_initial_view(model_converter)

if __name__ == "__main__":
    app.run_server(debug=True)