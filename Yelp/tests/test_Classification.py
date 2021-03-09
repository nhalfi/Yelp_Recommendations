#!/usr/bin/env python
# coding: utf-8

# DATA 515 - Winter 2021 - University of Washington
# 
# Yelp Healthy Food Recommendation
# 
# TEST: <b>TextClassification Module</b>

# ----

# In[ ]:


import os
import csv
import pandas as pd
import numpy as np
import unittest

import text_classification
from text_classification import text_classification


# In[ ]:


class MyTest_Classification(unittest.TestCase):
    
    def setup(self):
        print('START Test ...')
        
    def test_vectorize_function_no_input(self):
        """ 
            Test the vectorize_text function
            We call the function with no passing parameters
            We expect the code will raise an exception error
        """
        self.assertTrue(text_classification.vectorize_text())
      
    
    def test_vectorize_function_with_input(self):
        """ 
            Test the vectorize_text function
            We pass a dummy test in data frame to the function
            We expect it will return the dictionary value from vectorizer_text
        """
        result = text_classification.vectorize_text(['apple is healthy and delicious'])
        
        print('List of features in alphabet order: ', result.get_feature_names())
        print('Structure of vocabulary dictionary: ', result.vocabulary_)
        
        # Because the test sample is a short sentence (5 words)
        # so its vector number will be in the range 0 to 9

        value_check = result.vocabulary_['healthy']
        print('vectorized value of healthy: ', value_check)
        print('length: ', len(str(value_check)))
        
        # we can check the length of one randon word in the return result
        # if the numnber is one digit (aka less than 10), then we pass the test
        # if not equal one digit, then display the message of fail
        self.assertEqual(len(str(value_check)), 1, "Fail the test") 
           
            
    def test_main(self):
        """
            Test the main module - WIP
        """
        text_classification.main()
            
            
            
            
            
if __name__ == "__main__":
    unittest.main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




