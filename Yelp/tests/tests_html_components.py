import sys  # noqa: E402
sys.path.append('../')
from ui.html_components import ModelCoverter  # noqa: E402
import unittest  # noqa: E402
import pandas as pd  # noqa: E402


class TestModelCoverter(unittest.TestCase):

    def setUp(self):

        data = {
            'name': ["John's Chinese BBQ Restaurant", "Delmonico Steakhouse",
                     "Tacos", "Denny's"],
            'address': ['test1 st1', 'test2 st2', 'test3 st3', 'test4 st4'],
            'city': ['seattle', 'NewYork', 'testcity1', 'testcity2'],
            'state': ['WA', 'AZ', 'CO', 'VA'],
            'stars': [1, 2, 3, 4],
            'categories': ['asian,italian', 'american,iNdian', 'chinese,Sushi',
                           'no cuisine,test'],
            'prediction_score': [0.10, 0.15, 0.20, 1.00],
            'healthy_percent': ['10%', '15%', '20%', '100%']
            }
        self.df = pd.DataFrame.from_dict(data)

    def test_get_unique_cities_valid_case(self):
        model_converter = ModelCoverter(self.df)
        result = model_converter.get_unique_cities()
        assert(result)
        assert(len(result) == 4)

    def test_get_unique_states_valid_case(self):
        model_converter = ModelCoverter(self.df)
        result = model_converter.get_unique_states()
        assert(result)
        assert(len(result) == 4)

    def test_get_categories_valid_case(self):
        model_converter = ModelCoverter(self.df)
        result = model_converter.get_categories()
        assert(result)
        assert(len(result) == 8)

    def test_get_restaurant_cards_valid_case(self):
        model_converter = ModelCoverter(self.df)
        result = model_converter.get_restaurant_cards()
        assert(result)
        assert(len(result) == 4)
