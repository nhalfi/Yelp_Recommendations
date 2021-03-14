# Yelp_Recommendations
Final project for DATA 515 Software Design for Data Science course at University of Washington

<h2><i> Introduction </i></h2>
With the accelerating pace of life and the surge in demand for healthy lifestyles, more and more people have a need for nearby healthy restaurants. However, few tools incorporate this dimension into restaurant searches. The goal of our project is to provide a way for users to discover healthy restaurants within the existing Yelp directory. Using Yelp data, our platform will provide restaurant health ratings to eaters based on the results of our machine learning model. The relevant  data in our project consists of business data and photo metadata, including captions. We will apply Natural Language Processing, Text Classification, and Machine Learning techniques  to analyze the descriptive text in the captions of food photos to determine whether the food is healthy or not. 

<h2><i>Data</i></h2>

<i> <h4> Yelp Dataset </h4></i> The main dataset for our project is the public [Yelp Open Dataset](https://www.yelp.com/dataset). This dataset is available to the public in JSON files. The data captures details of almost 209K Businesses across ~10 cities capturing ~ 8M reviews and ~200K pictures. Though original Yelp dataset is rich in many data dimensions, not all the data features are useful, instead, finding the right data features for the job is as important as building an effective model. Our project focuses on the classification of healthy or unhealthy restaurants based on the photos shared by Yelpers. Therefore, business data and photo data are key features for our model. 

<i> <h4> Nutritionix Dataset </h4></i> The second dataset is the [Nutritionix dataset](https://www.nutritionix.com/business/api) which contains nutrition information from chain restaurants across the US.  We are using it to train our classification model that will assign healthy or unhealthy labels. <br>

In order to apply these two dataset proeprly, we encourage all users to review [Yelp Dataset: Terms of Service](https://terms.yelp.com/tos/en_us/20200101_en_us/) and [Nutritionix Dataset: Terms and Conditions](https://www.nutritionix.com/apiterms) for a bette usage experience. 


<h2><i>Organization of the Project</i></h2>
The project has the following structure (8 directories, 36 files): <br>

```
  .
└── Yelp_Recommendations-main
    ├── LICENSE
    ├── README.md
    ├── Yelp
    │   ├── __init__.py
    │   ├── app.py
    │   ├── data
    │   │   ├── Yelp_Healthy_restaurant_predictions.csv
    │   │   ├── __init__.py
    │   │   ├── nutritionix_health.csv
    │   │   ├── nutritionix_tokenized.csv
    │   │   ├── restaurants_dao.py
    │   │   ├── yelp_business_clean.csv
    │   │   ├── yelp_final_tokenized.csv
    │   │   ├── yelp_joined_clean.csv
    │   │   └── yelp_photos_clean.csv
    │   ├── data_processing
    │   │   ├── __init__.py
    │   │   ├── data_processing.py
    │   │   └── download_nutritionix_data.ps1
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── business.json
    │   │   ├── empty.csv
    │   │   ├── logic_test.csv
    │   │   ├── nutrition.json
    │   │   ├── photos.json
    │   │   ├── restaurant_sample.csv
    │   │   ├── restaurant_sample2.csv
    │   │   ├── sample_nutritionix_data.csv
    │   │   ├── sample_yelp_data.csv
    │   │   ├── test_data_processing.py
    │   │   ├── test_restaurants_dao.py
    │   │   └── test_text_classification.py
    │   ├── text_classification
    │   │   ├── __init__.py
    │   │   └── text_classification.py
    │   └── ui
    │       ├── __init__.py
    │       └── html_components.py
    ├── azure-pipelines.yml
    ├── examples
    │   └── README.md
    └── setup.py
```

<h2><i>Installation</i></h2> WIP

<h2><i>Examples (How to use Yelp-Recommendations)</i></h2> 

To better understand how to use ```Yelp-Recommendations``` , please refer to the [usage examples](https://github.com/nhalfi/Yelp_Recommendations/tree/main/examples) provided on this GitHub page. Through the example, you can grasp the basic steps to run this tool as followings:

  * Launching the App <br>
    OR
  * Reproducing our Model
    * Download Extracted Yelp JSON Files
    * Download Nutritionix Data
    * Process the Datasets and Run the Text Classification Model

<h2><i>Limitations and Future Work</i></h2> 

  * The cities covered by the project are very limited <br>
  * Additional training datasets that are closer to Yelp <br>
  * Image classification of photos in addition to text classification <br>

<h2><i>Acknowledgements</i></h2> 

We are very grateful to our course instructors, Dr. Mark Friedman and Bernease Herman, of the University of Washington, for their valuable guidance of DATA 515 project, which greatly improved our understanding of software design and specific practice skills in data science. <br>
<br>
Our data sources are mainly the public Yelp Open Dataset and the Nutritionix dataset, we sincerely thank these open sources for supporting our project.

<h2><i>Contact (optional)</i></h2> WIP
