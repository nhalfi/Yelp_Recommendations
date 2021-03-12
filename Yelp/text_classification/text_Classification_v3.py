#!/usr/bin/env python
# coding: utf-8


import json 
import pandas as pd 
import nltk
import random , math
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn import metrics


# Declare all variables outside of the function main, then reference them as glabal variables inside each function

# Function read_dataset variables
x_train = pd.DataFrame()
x_test = pd.DataFrame()
yelp_test = pd.DataFrame()
yelp = pd.DataFrame()

# Function vectorize_text variables
training_data = pd.DataFrame()
test_data = pd.DataFrame()
yelp_test_data = pd.DataFrame()

# Function fit_and_evaluate_model variables
conf_matrix = []
accuracy = []
model = []

#Function predict_on_Yelp variables
yelp_final = []

random.seed(100)



#-----------------------------------------------------------------------------------------------------
def split_test_train_dataset(res_health,yelp):
    
      """
            This function splits Nutritionix dataset into test and train dataset, also creates a test dataset from yelp dataset to later generate predictions on
            - x_train : Training dataset from Nutritionix 
            - x_test : Test dataset for Nutritionix
            - yelp_test : Test Dataset from yelp
        """ 
    
    global x_train, x_test, yelp_test

    feature_data = res_health[['filtered_caption','healthy']]
    x_train , x_test = train_test_split(feature_data,test_size=0.5)
    yelp_test = pd.DataFrame(yelp['filtered_caption'])
        
    return(x_train, x_test, yelp_test)


#-----------------------------------------------------------------------------------------------------
def vectorize_text(x_train, x_test, yelp_test):
      """
            - Function to invoke the CountVectorize from the library to vectorize data for model
            - Return the vecterization data for transformation for training, test and yelp data
         
        """
    
    global training_data, test_data, yelp_test_data
    
    #vectorize text for nutritionix
    vector = CountVectorizer()
    vector.fit(x_train["filtered_caption"])
    vector = CountVectorizer(vocabulary=vector.vocabulary_) #vocabulary is a parameter, it should be vocabulary_ as it is an attribute.
    
    # Apply vectorization
    training_data = vector.transform(x_train["filtered_caption"])
    test_data = vector.transform(x_test["filtered_caption"])
    
    # Perform vectorization on yelp dataset and generating perdictions by applying naive bayes classfier
    # Apply vectorization for the Yelp
    yelp_test_data = vector.transform(yelp_test["filtered_caption"])
    
    
    return(training_data, test_data, yelp_test_data)


#-----------------------------------------------------------------------------------------------------
def fit_and_evaluate_model(training_data, test_data, x_test, label_col):
    """
    - Evaluates model generated with training data against test data
    - model: model object
    - x_test: Nutritionix test dataset to calculate confusion metrics and accuracy
    - test_data: Nutrionix vectorized captions to predict labels
    - training dataset : Nutrionix vectorized captions to train model
    - label_col: labels of Nutrionix dataset to train model
    - returns confusion matrix and accuracy score for model applied to test dataset
    """
    
    global conf_matrix, accuracy, model

    #fit and evaluate model
    model = MultinomialNB().fit(training_data, label_col)  
    #print(evaluate_model(model,x_test,test_data,'healthy'))
    
    # Predict labels for Test data
    test_predict = model.predict(test_data)
    
    # Check accuracy of model on Test data
    conf_matrix = confusion_matrix(x_test['healthy'],test_predict)
    accuracy = metrics.accuracy_score(x_test['healthy'],test_predict)
    
    return(conf_matrix, accuracy, model)


#-----------------------------------------------------------------------------------------------------
def predict_on_Yelp(model, yelp_test_data, yelp):
    
    global yelp_final
    
    # Predicting with Naive Bayes classifier
    yelp_predict = model.predict(yelp_test_data)

    # Storing predictions
    yelp["prediction_score"] = yelp_predict
    
    # Generate final yelp dataset with predicted flags and average health scores for each business

    yelp_final = yelp.groupby(['business_id','name', 'address','city','state','postal_code','latitude','longitude','stars','review_count','categories'])[['prediction_score']].mean()
    yelp_final['healthy_percent'] = pd.Series(["{0:.2f}%".format(val * 100) for val in yelp_final['prediction_score']], index = yelp_final.index)
    yelp_final

    # Export yelp predictions to CSV
    yelp_final.to_csv('../data/Yelp_Healthy_restaurant_predictions.csv',  header=True)
    
    return yelp_final


#-----------------------------------------------------------------------------------------------------
def main():
    
    
    try:
        res_health = pd.read_csv("data/nutritionix_tokenized.csv")
        yelp = pd.read_csv("data/yelp_final_tokenized.csv")
        
    except Exception:
        print("Ensure you have cloned the Data folder.")
        
    else:
        
   
        # Read in the dataset for both the nutritionix and yelp
    
        x_train, x_test, yelp_test = split_test_train_dataset(res_health,yelp)
    
        # Call the vectorize text function
        training_data, test_data, yelp_test_data = vectorize_text(x_train, x_test, yelp_test)
        label_col =x_train['healthy']
    
         # Call the fit and evaluate function for Nutritionix
        conf_matrix, accuracy, model = fit_and_evaluate_model(training_data, test_data, x_test, label_col)

        # Call the fit and evaluate function for Yelp                        
        yelp_final = predict_on_Yelp(model, yelp_test_data, yelp)
        
        
        print(conf_matrix)
        print(accuracy)
        print(type(conf_matrix))
        print(type(accuracy))
        print(type(yelp_final))


if __name__ == "__main__":
    main()

