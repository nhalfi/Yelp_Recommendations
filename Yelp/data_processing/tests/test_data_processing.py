import unittest
from Yelp.data_processing.data_processing import*
import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('punkt')

class test_data_processing(unittest.TestCase):

   def test_text_process(self):
       a = pd.read_csv('restaurant_sample.csv')
       a= pd.DataFrame(a)
       print(a)

       cols_a = a.columns
       self.assertTrue('item_name' in cols_a)

       b= text_process(a,'item_name')
       self.assertTrue(type(b) is pd.DataFrame)


       cols_b = b.columns
       self.assertTrue('filtered_caption' in cols_b)

       with self.assertRaises(ProcessingError):
       # an empty csv raises rocessingError
           emptycsv = pd.read_csv('empty.csv')
           empty = text_process(emptycsv, 'item_name')






