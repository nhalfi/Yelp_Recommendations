import pandas as pd

YELP_DATA_FILE = 'data/Yelp_Healthy_restaurant_predictions.csv'


def load_data_from_file(file_path=YELP_DATA_FILE):
    df = pd.read_csv(file_path)
    return df


def search(regex: str, df, case=False):
    """Search all the text columns of `df`, return rows with any matches."""
    textlikes = df.select_dtypes(include=[object, "string"])
    return df[
        textlikes.apply(
            lambda column: column.str.contains(
                regex,
                regex=True,
                case=case,
                na=False)
        ).any(axis=1)
    ]


def get_yelp_dataframe(user_df, user_selections=None):
    """Function takes an user provided dataframe.
    Filters the dataframe with user made selctions.

    Args:
        user_df (DataFrame): user provided pandas dataframe.
        user_selections (dict, optional): Filter values to apply.
                                            Defaults to None.

    Returns:
        DataFrame: Returns a filtered dataframe.
    """
    filtered_df = user_df
    if user_selections:
        search_string = user_selections.get('search_string', None)
        if search_string:
            filtered_df = search(search_string, filtered_df)

        states_selected = user_selections.get('states_selected', None)
        print(states_selected)
        if states_selected:
            bool_array = filtered_df['state'].isin(states_selected)
            filtered_df = filtered_df[bool_array]
            print(filtered_df)
        cities_selected = user_selections.get('cities_selected', None)

        if cities_selected:
            print('cities {}'.format(cities_selected))
            bool_array = filtered_df['city'].isin(cities_selected)
            filtered_df = filtered_df[bool_array]

        health_score = user_selections.get('health_score_selected', 0)
        if health_score:
            bool_array = filtered_df['prediction_score'] >= (health_score/100)
            filtered_df = filtered_df[bool_array]

        ratings_selected = user_selections.get('ratings', 0)
        if ratings_selected:
            bool_array = filtered_df['stars'] >= ratings_selected
            filtered_df = filtered_df[bool_array]

    return filtered_df
