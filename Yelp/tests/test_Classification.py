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
from text_classification import text_Classification_v3


# In[ ]:


class MyTest_Classification(unittest.TestCase):
    
    def setup(self):
        print('START Test ...')
           
    #...............................................................................................
    def test_split_test_train_dataset(self):
        """
            Test the read_dataset function
            - Call the function and validate the return value from the function
            - If the read dataset function working correctly, it will return the sub-datasets
            - The sub datasets size will be greater than 0
            - If the sub datasets are 0 (aka. empty), and exception is raise to fail the test
        """
        
        validate_x_train = 0
        validate_x_test = 0
        validate_yelp_test = 0
        
        validate_x_train, validate_x_test, validate_yelp_test = text_Classification_v3.read_dataset()
        
        print(validate_x_train.count()[0])
        print(validate_x_test.count()[0])
        print(validate_yelp_test.count()[0])
        
        
        self.assertGreater(validate_x_train.count()[0], 0, 'Fail: x_train sub-dataset')
        self.assertGreater(validate_x_test.count()[0], 0, 'Fail: x_test sub-dataset')
        self.assertGreater(validate_yelp_test.count()[0], 0, 'Fail: y_test sub-dataset')
    
    #...............................................................................................
#    def test_vectorize_text(-------):
#         """
#             Test the vectorize_text function
#             - Function to invoke the CountVectorize from the library to vectorize data for model
#             - Return the vecterization data for transformation for training, test and yelp data
#             - An exception will raise when the output is not in a vector format
#         """
    
    
    #...............................................................................................
#     def test_fit_and_evaluate_model(-------):
#         """
#             Test the fit_and_evaluate_model function
#             - This function takes in the vecterized values and perform fit then evaluate model
#             - It returns a confusion matrix, accuracy, and model
#             - An exception will raise when it fails the model
#         """
    
    
    #...............................................................................................
#     def test_predict_on_Yelp(------):
#         """
#             Test the prediction model
#             - The function will predict the model with Naive Bayes classifier
#             - An exception will raise if the final result is not correctly processed
#         """
    
    
    
    
    
    
    
    
    
    
    
    
    
# Sample code from previous work    
#-----------------------------------------------------------------------------------------------------------        
#     def test_vectorize_function_no_input(self):
#         """ 
#             Test the vectorize_text function
#             We call the function with no passing parameters
#             We expect the code will raise an exception error
#         """
        
#         self.assertRaises(Exception, text_classification.vectorize_text())
      
    
#     def test_vectorize_function_with_input(self):
#         """ 
#             Test the vectorize_text function
#             We pass a dummy test in data frame to the function
#             We expect it will return the dictionary value from vectorizer_text
#         """
#         result = text_classification.vectorize_text(['apple is healthy and delicious'])
        
#         print('List of features in alphabet order: ', result.get_feature_names())
#         print('Structure of vocabulary dictionary: ', result.vocabulary_)
        
#         # Because the test sample is a short sentence (5 words)
#         # so its vector number will be in the range 0 to 9

#         value_check = result.vocabulary_['healthy']
#         print('vectorized value of healthy: ', value_check)
#         print('length: ', len(str(value_check)))
        
#         # we can check the length of one randon word in the return result
#         # if the numnber is one digit (aka less than 10), then we pass the test
#         # if not equal, display the message of fail
#         self.assertEqual(len(str(value_check)), 1, "Fail the test") 
        
        
            
if __name__ == "__main__":
    unittest.main()

