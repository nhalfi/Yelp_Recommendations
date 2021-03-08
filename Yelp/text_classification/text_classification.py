# Module: TextClassification.py
# Purpose: create text classification model using Naive Bayes algorithm

# import libraries 
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

def vectorize_text(vector_col):
    """
    -vectorizes text to float to prepare for model generation
    -vector_col: column of a dataframe that contains text to be vectorized
    -returns vector
    """

    vector = CountVectorizer()
    vector.fit(vector_col)
    vector = CountVectorizer(vocabulary=vector.vocabulary_)
    
    return(vector)

def evaluate_model(model,x_test, test_data,label_col):
    """
    -evaluates model generated with training data against test data
    -model: model object
    -x_test: test split dataset
    -test_data: vectorized column
    -label_col: column in x_test that contains labels
    -returns confusion matrix and accuracy score for model applied to test dataset
    """

    # Predict labels for Test data
    test_predict = model.predict(test_data)

    # Check accuracy of model on Test data
    conf_matrix = confusion_matrix(x_test[label_col],test_predict)
    accuracy = metrics.accuracy_score(x_test[label_col],test_predict)

    return(conf_matrix,accuracy)

def main():
    try:
        res_health = pd.read_csv("../Data/nutritionix_tokenized.csv")
    except Exception:
        print("Ensure you have cloned the Data folder.")
    else:
        # Splitting dataset into training and test
        feature_data = res_health[['filtered_caption','healthy']]
        feature_data.head()
        random.seed(100)
        x_train ,x_test = train_test_split(feature_data,test_size=0.5)

        #vectorize text
        vector = vectorize_text(x_train['filtered_caption'])
        # Apply vectorization
        training_data = vector.transform(x_train["filtered_caption"])
        test_data = vector.transform(x_test["filtered_caption"])

        #fit and evaluate model
        model = MultinomialNB().fit(training_data, x_train['healthy'])  
        print(evaluate_model(model,x_test,test_data,'healthy'))

        # Load the yelp dataset
        try:
            yelp = pd.read_csv("../Data/yelp_final_tokenized.csv")
        except Exception:
            print("Ensure you have cloned the Data folder.")
        else:
            yelp_test = pd.DataFrame(yelp['filtered_caption'])

            # Perform vectorization on yelp dataset and generating perdictions by applying naive bayes classfier
            # Apply vectorization
            yelp_test_data = vector.transform(yelp_test["filtered_caption"])

            # Predicting with Naive Bayes classifier
            yelp_predict = model.predict(yelp_test_data)

            # Storing predictions
            yelp["prediction_score"] = yelp_predict

            # Generate final yelp dataset with predicted flags and average health scores for each business

            yelp_final = yelp.groupby(['business_id','name', 'address','city','state','postal_code','latitude','longitude','stars','review_count','categories'])[['prediction_score']].mean()
            yelp_final['healthy_percent'] = pd.Series(["{0:.2f}%".format(val * 100) for val in yelp_final['prediction_score']], index = yelp_final.index)
            yelp_final

            # Export yelp predictions to CSV
            yelp_final.to_csv('../Data/Yelp_Healthy_restaurant_predictions.csv',  header=True)


if __name__ == "__main__":
    main()