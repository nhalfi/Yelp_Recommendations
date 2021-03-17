import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_html_components as html
import dash_leaflet.express as dlx

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

icon = {
    "iconUrl": "https://leafletjs.com/examples/custom-icons/leaf-green.png",
    "shadowUrl": "https://leafletjs.com/examples/custom-icons/leaf-shadow.png",
    "iconSize": [38, 95],  # size of the icon
    "shadowSize": [50, 64],  # size of the shadow
    # point of the icon which will correspond to marker's location
    "iconAnchor": [22, 94, ],
    "shadowAnchor": [4, 62],  # the same for the shadow
    # point from which the popup should open relative to the iconAnchor
    "popupAnchor": [-3, -76, ],
}


class ModelCoverter:

    def __init__(self, df):
        self.df = df

    def get_unique_cities(self):
        """
            Function that produces list of dictionaries with city name.
            This list can be used as arguments for dash dropdown component.
        Returns:
            list: list of cities as a dictionary.
        """
        cities = list(self.df['city'].unique())
        cities_groups_all = []
        if cities:
            cities_groups_all = [
                {'label': k, 'value': k} for k in sorted(cities)
                ]
        return cities_groups_all

    def get_unique_states(self):
        """
            Function that produces list of dictionaries with state name.
            This list can be used as arguments for dash dropdown component.
        Returns:
            list: list of states as a dictionary.
        """
        states = list(self.df['state'].unique())
        states_groups_all = []
        if states:
            states_groups_all = [
                {'label': k, 'value': k} for k in sorted(states)
                ]
        return states_groups_all

    def get_cluster_makers(self):
        """
            Utility fucntion that produces leaflet markers as geojson objects.
            Markers contain tooltip and popup elements.
            Color and other aspects of markers can be modified here.
        Returns:
            object: geojson for leaflet.
        """
        if self.df is not None:
            dicts = self.df.to_dict('rows')
            for item in dicts:
                item["tooltip"] = item["name"]  # bind tooltip
                item["popup"] = item["healthy_percent"]
            geojson = dlx.dicts_to_geojson(
                dicts,
                lon='longitude',
                lat='latitude'
                )
            return geojson

    def get_categories(self):
        """
            This function  creates a set of cuisine categories from the data.
            Categories column has categories offered by each restaurant.
        Returns:
            list: list of categories
        """
        categories = set()
        for csv_category in self.df['categories']:
            for category in csv_category.split(','):
                categories.add(category)
        return list(categories)

    def get_restaurant_cards(self, limit=20):
        """
        Creates a list of bootstrap cards.
        Each card shows details of restaurant.
        The list is ordered by the health percent column, in descending order.

        Args:
            limit (int, optional): Number of cards to return. Defaults to 20.

        Returns:
            object: A boostrap cards object.
        """
        sorted_df = self.df.sort_values(
            by=['prediction_score'],
            ascending=False
            ).head(limit)
        cards = []
        for _, row in sorted_df.iterrows():
            card_content = [
                dbc.CardHeader(html.H5(row['name'])),
                dbc.CardBody(
                    [
                        html.P(row['address'], className="card-title"),
                        html.P(
                            "health score {}".format(row['healthy_percent']),
                            className="card-text",
                            ),
                    ]
                ),
                ]
            cards.append(card_content)
        card_columns = []
        for card in cards:
            card_columns.append(dbc.Card(card, outline=True, color="primary"))
        return card_columns


class Components:

    @staticmethod
    def get_leaflet_map(geojson):
        """Creates a dash leaflet object used in the landing page.

        Args:
            geojson (object): takes python object that is a geojson.

        Returns:
            object: Dash leaflet object.
        """

        return html.Div([
            dl.Map(center=[39, -98], zoom=4, children=[
                dl.TileLayer(),
                dl.GeoJSON(
                    data=geojson,
                    cluster=True,
                    id="geojson",
                    zoomToBounds=True,
                    zoomToBoundsOnClick=True,
                    superClusterOptions={"radius": 100})
                ])
            ], id='map',
            style={
                'width': '100%',
                'height': '50vh',
                'margin': "auto",
                "display": "block",
                "position": "relative"
                })

    @staticmethod
    def get_cities_list(cities):
        """Creates a dropdown list of cities.

        Args:
            cities (list): list of dictionaries needed for dash dropdown.

        Returns:
            Object: Dash drop down component.
        """
        return dcc.Dropdown(
            id='cities-dropdown',
            options=cities,
            value=[''],
            multi=True,
            placeholder="Select Cities",
            style={
                'font-size': '13px',
                'white-space': 'nowrap',
                'text-overflow': 'ellipsis'
                }
        )

    @staticmethod
    def get_states_list(states):
        """Creates a drop down with provided states.

        Args:
            states (list): List of dictionaries needed for dropdown.

        Returns:
            object : Dash dropdown with states.
        """
        return dcc.Dropdown(
            id='states-dropdown',
            options=states,
            value=[''],
            multi=True,
            placeholder="Select State",
            style={
                'font-size': '13px',
                'white-space': 'nowrap',
                'text-overflow': 'ellipsis'
                }
        )

    @staticmethod
    def get_categories_list(categories):
        """Creates a drop down with categories states.

        Args:
            categories (list): List of dictionaries needed for dropdown.

        Returns:
            object : Dash dropdown with states.
        """
        return dcc.Dropdown(
            id='categories-dropdown',
            options=categories,
            value=['All'],
            multi=True,
            placeholder="Select State",
            style={
                'font-size': '13px',
                'white-space': 'nowrap',
                'text-overflow': 'ellipsis'
                }
        )

    @staticmethod
    def get_ratings_radioitems():
        """Creates radio button items for ratings.

        Returns:
            object: returns dash bootstrap radioitems.
        """
        return dbc.FormGroup(
            [
                dbc.Label("Ratings"),
                dbc.RadioItems(
                    options=[
                        {'label': '5 Stars', 'value': 5},
                        {'label': '4 stars and up', 'value': 4},
                        {'label': '3 stars and up', 'value': 3},
                        {'label': '2 stars and up', 'value': 2},
                        {'label': '1 stars and up', 'value': 1},
                    ],
                    id="ratings",
                ),

            ]
        )

    @staticmethod
    def get_healthy_restaurant_cards(cards, limit=10):
        return dbc.CardColumns(cards, id='restaurant_cards')

    @staticmethod
    def get_text_input():
        """Createa a text input for users to serach.

        Returns:
            Dash text ui element.
        """
        return html.Div(
            [
                dbc.Input(
                    id="input",
                    placeholder="Search cuisine or restaurants...",
                    type="text",
                    debounce=True
                ),
                html.Br(),
                html.P(id="output"),
            ])

    @staticmethod
    def get_health_slider():
        """Creates a dash slider object for health score filtering.

        Returns:
            A dash object of a slider ui element.
        """
        return dcc.Slider(
            id='health-slider',
            min=0,
            max=100,
            step=10,
            value=0,
            marks={
                0: {'label': '0', 'style': {'color': '#77b0b1'}},
                10: {'label': '10'},
                20: {'label': '20'},
                30: {'label': '30'},
                40: {'label': '40'},
                50: {'label': '50'},
                60: {'label': '60'},
                70: {'label': '70'},
                80: {'label': '80'},
                90: {'label': '90'},
                100: {'label': '100', 'style': {'color': '#77b0b1'}}
            }
        )


def get_initial_view(model_converter):
    """The function builds the view that is displayed on page load.
    The page contains a side navigation bar and main content page.

    Args:
        ModelConverter: A model converter object used for generatig view.
    """
    geojson = model_converter.get_cluster_makers()
    sidebar = html.Div(
        [
            html.H2("Yelp", className="display-4"),
            html.Hr(),
            dbc.Nav(
                [
                    Components.get_text_input(),
                    Components.get_states_list(
                        model_converter.get_unique_states()),
                    Components.get_cities_list(
                        model_converter.get_unique_cities()),
                    html.Br(),
                    html.Div(
                        [
                            html.P("Health score %"),
                            Components.get_health_slider()
                        ]),
                    html.Br(),
                    html.Div(
                        [
                            Components.get_ratings_radioitems()
                        ])
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    map_restaurants = html.Div([
        html.H1('Yelp Restaurants'),
        html.P("""The results shown below are from a machine learning
        model and thus may not necessarily be nutritionally accurate."""),
        Components.get_leaflet_map(geojson),
    ], id="page-content", style=CONTENT_STYLE)

    body = dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    [
                        map_restaurants
                    ]
                ),
            ),
            dbc.Row(
                dbc.Col(
                    [
                        Components.get_healthy_restaurant_cards(
                            model_converter.get_restaurant_cards())
                    ]
                ),
            )
        ],
    )
    return html.Div([sidebar, body])
