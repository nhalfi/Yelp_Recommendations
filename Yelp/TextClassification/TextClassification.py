# Module: TextClassification.py
# Purpose: create text classification model using Naive Bayes algorithm

def main():
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

    res_health = pd.read_csv("trainingdataset_tokenized.csv")

    # Splitting dataset into training and test


    feature_data = res_health[['filtered_item_name','healthy']]
    feature_data.head()

    random.seed(100)
  
    x_train ,x_test = train_test_split(feature_data,test_size=0.5)

    # Vectorize Training Dataset and applying vectrization on training and test dataset

    # Perform vectorization
    vector = CountVectorizer()
    vector.fit(x_train["filtered_item_name"])
    vector = CountVectorizer(vocabulary=vector.vocabulary_) #vocabulary is a parameter, it should be vocabulary_ as it is an attribute.


    # Apply vectorization
    training_data = vector.transform(x_train["filtered_item_name"])
    test_data = vector.transform(x_test["filtered_item_name"])

    # Build Naive Bayes classifier 
    # Fitting classifier on Training data
    model = MultinomialNB().fit(training_data, x_train['healthy'])

    # Predicting labels for Test data
    test_predict = model.predict(test_data)

    # Checking accuracy of model on Test data
    confusion_matrix(x_test['healthy'],test_predict)
    metrics.accuracy_score(x_test['healthy'],test_predict)

    # Loading the yelp dataset

    yelp = pd.read_csv("yelp_final_tokenized.csv")
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
    yelp_final.to_csv('Yelp_Healthy_restaurant_predictions.csv',  header=True)


if __name__ == "__main__":
    main()