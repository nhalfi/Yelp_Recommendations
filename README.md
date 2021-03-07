# Yelp_Recommendations
Final project for DATA 515 Software Design for Data Science course at University of Washington

<h4><i> Introduction </i></h4>
With the accelerating pace of life and the surge in demand for healthy lifestyles, more and more people have a need for nearby healthy restaurants. However, few tools incorporate this dimension into restaurant searches. The goal of our project is to provide a way for users to discover healthy restaurants within the existing Yelp directory. Using Yelp data, our platform will provide restaurant health ratings to eaters based on the results of our machine learning model. The relevant  data in our project consists of business data and photo metadata, including captions. We will apply Natural Language Processing, Text Classification, and Machine Learning techniques  to analyze the descriptive text in the captions of food photos to determine whether the food is healthy or not. 

<h4><i>Data</i></h4>

<i> <h2> Yelp Dataset </h2></i> : The main dataset for our project is the public Yelp Open Dataset. This dataset is available to the public in JSON files. The data captures details of almost 209K Businesses across ~10 cities capturing ~ 8M reviews and ~200K pictures. Though original Yelp dataset is rich in many data dimensions, not all the data features are useful, instead, finding the right data features for the job is as important as building an effective model. Our project focuses on the classification of healthy or unhealthy restaurants based on the photos shared by Yelpers. Therefore, business data and photo data are key features for our model. 


The second dataset is the Nutritionix dataset which contains nutrition information from chain restaurants across the US.  We are using it to train our classification model that will assign healthy or unhealthy labels.

