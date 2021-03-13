import pandas as pd


def load_data_from_file():
    yelp_data_file = 'data/Yelp_Healthy_restaurant_predictions.csv'
    df =  pd.read_csv(yelp_data_file)
    return df

def search(regex: str, df, case=False):
    """Search all the text columns of `df`, return rows with any matches."""
    textlikes = df.select_dtypes(include=[object, "string"])
    return df[
        textlikes.apply(
            lambda column: column.str.contains(regex, regex=True, case=case, na=False)
        ).any(axis=1)
    ]

def get_yelp_dataframe(user_df, user_selections = None):
    filtered_df = user_df    
    if user_selections:
        search_string = user_selections.get('search_string', None)
        if search_string:
            filtered_df = search(search_string,filtered_df)

        states_selected = user_selections.get('states_selected', None)
        print(states_selected)
        if states_selected:
            filtered_df = filtered_df[filtered_df['state'].isin(states_selected)]
            print(filtered_df)
        cities_selected = user_selections.get('cities_selected', None)
        
        if cities_selected:
            print('cities {}'.format(cities_selected))
            filtered_df = filtered_df[filtered_df['city'].isin(cities_selected)]
        
        health_score_selected = user_selections.get('health_score_selected', 0)
        if health_score_selected:
            filtered_df = filtered_df[filtered_df['prediction_score'] >= (health_score_selected/100)]
        
        ratings_selected = user_selections.get('ratings',0)
        if ratings_selected:
            filtered_df = filtered_df[filtered_df['stars'] >= ratings_selected]

    # print(filtered_df)
    return filtered_df

    

