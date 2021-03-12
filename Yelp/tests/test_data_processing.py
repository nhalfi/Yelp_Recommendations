#import libraries
import unittest
import sys
sys.path.append('../')
from data_processing import data_processing as dp
import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('punkt')


class test_data_processing(unittest.TestCase):

    def test_text_process(self):
        a = pd.read_csv('restaurant_sample.csv')
        a= pd.DataFrame(a)
        print(a)

        #check that relevant column name exits
        cols_a = a.columns
        self.assertTrue('item_name' in cols_a)

        b= dp.text_process(a,'item_name')
        #test that return type is correct
        self.assertTrue(type(b) is pd.DataFrame)


        cols_b = b.columns
        #test that calculated column is added
        self.assertTrue('filtered_caption' in cols_b)

        with self.assertRaises(dp.ProcessingError):
            # an empty csv raises rocessingError
            emptycsv = pd.read_csv('empty.csv')
            dp.text_process(emptycsv, 'item_name')

    def test_calculate_health(self):
        #file with missing columns
        df = pd.read_csv('restaurant_sample.csv')
        with self.assertRaises(Exception):
            dp.calculate_health(df)

        #valid file, test that it returns df and adds calculated column
        df = pd.read_csv('restaurant_sample2.csv')
        df_health = dp.calculate_health(df)
        self.assertTrue(type(df_health) is pd.DataFrame)
        self.assertTrue('healthy' in df_health.columns)

    def test_clean_yelp(self):
        #pass invalid files
        df1 = pd.read_csv('restaurant_sample.csv')
        df2 = pd.read_csv('restaurant_sample2.csv')
        with self.assertRaises(Exception):
            dp.clean_yelp(df1,df2)

        #pass valid files but with no matching business IDs
        df_b = pd.read_json('business.json',lines=True)
        df_p = pd.read_json('photos.json',lines=True)
        df_join = dp.clean_yelp(df_b,df_p)
        self.assertTrue(len(df_join)==0)

    def test_load_datasets(self):
        #test non-existent filepaths
        with self.assertRaises(Exception):
            df1,df2,df3 = dp.load_datasets('../data/test_data.json','../data/test_photos.json', '../data/test_restaurants_items.json')
        #two valid filepaths and one invalid
        with self.assertRaises(Exception):
            df1,df2,df3 = dp.load_datasets('business.json','photos.json', 'restaurants_items.json')

        #test with valid data that returns correct data type
        df1,df2,df3 = dp.load_datasets('business.json','photos.json', 'nutrition.json')
        self.assertTrue(type(df1) is pd.DataFrame)
        self.assertTrue(type(df2) is pd.DataFrame)
        self.assertTrue(type(df3) is pd.DataFrame)

    def test_output_csv(self):
        #pass invalid arguments
        with self.assertRaises(Exception):
            dp.output_csv(1,2,3)

        #pass valid arguments
        df1,df2,df3 = dp.load_datasets('business.json','photos.json', 'nutrition.json')
        df4 = df3.copy()
        dp.output_csv(df1,df2, df3,df4)



if __name__ == '__main__':
    unittest.main()
