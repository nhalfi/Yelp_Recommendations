import unittest
import sys
sys.path.append('../')
import pandas as pd
from data.restaurants_dao import get_yelp_dataframe


class TestFilter(unittest.TestCase):

    def setUp(self):

        data = {
            'name': ["John's Chinese BBQ Restaurant", "Delmonico Steakhouse",
                     "Tacos", "Denny's"],
            'address': ['test1 st1', 'test2 st2', 'test3 st3', 'test4 st4'],
            'city': ['seattle', 'NewYork', 'testcity1', 'testcity2'],
            'state': ['WA', 'AZ', 'CO', 'VA'],
            'stars': [1, 2, 3, 4],
            'categories': ['asian,italian', 'american,iNdian', 'chinese,Sushi',
                           'no cuisine'],
            'prediction_score': [0.10, 0.15, 0.20, 1.00]
            }
        self.df = pd.DataFrame.from_dict(data)

    def test_state_lookup_for_valid_state(self):
        user_selections = {'states_selected': ['WA']}
        result = get_yelp_dataframe(self.df, user_selections)
        assert(result.shape[0] == 1)
        assert('WA' in result['state'][0])

    def test_state_lookup_for_valid_city(self):
        user_selections = {'cities_selected': ['NewYork']}
        result = get_yelp_dataframe(self.df, user_selections)
        assert(result.shape[0] == 1)
        assert('NewYork' in result['city'][1])

    def test_state_lookup_for_valid_ratings(self):
        user_selections = {'ratings': 4}
        result = get_yelp_dataframe(self.df, user_selections)
        assert(result.shape[0] == 1)
        assert(result['stars'][3] == 4)

    def test_state_lookup_for_valid_string_search(self):
        user_selections = {'search_string': 'asian'}
        result = get_yelp_dataframe(self.df, user_selections)
        assert(result.shape[0] == 1)


if __name__ == '__main__':
    unittest.main()
