# Yelp_Recommendations
Final project for DATA 515 Software Design for Data Science course at University of Washington (Winter 2021)

<h2> Introduction </h2>
With the increasing emphasis on health diet and lifestyle, more and more people have a need for nearby healthy restaurants. However, few tools incorporate this dimension into restaurant searches. The goal of our project is to provide a way for users to discover healthy restaurants within the existing Yelp directory. We achieved this by providing restaurant health ratings to eaters based on the results of our machine learning model that applies Natural Language Processing and Text Classification techniques. Specifically, we analyzed the descriptive text in the captions of food photos on Yelp to infer whether the food is healthy or not. We then averaged the scores for a given restaurant to provide a health score ranging from 0-100%.

<h2>Data</h2>

<i> <h4> Yelp Dataset </h4></i> The main dataset for our project is the public [Yelp Open Dataset](https://www.yelp.com/dataset). This dataset is available via JSON files. The data captures details of almost 209K Businesses across ~10 cities capturing ~ 8M reviews and ~200K pictures. In our project, we leveraged the business details and photo captions as features to classify healthy or unhealthy restaurants based on the photos shared by Yelpers. 

<i> <h4> Nutritionix Dataset </h4></i> The second dataset is the [Nutritionix dataset](https://www.nutritionix.com/business/api) which contains nutrition information from chain restaurants across the US.  We used this dataset to train our classification model that assigns healthy or unhealthy labels. To achieve this, we performed feature engineering on the dataset to generate training labels based on the nutrition information for each item. To learn more about the nutrition logic used, please refer to our Component Documentation. <br>

<i> <h4> Terms of Use </h4></i>
The Yelp Open Dataset is publicly accessible and allows public use for academic purposes. The Nutritionix API is publicly accessible, but does not allow caching of its data. Therefore, we have not stored any of its data in our repository, but we provide instructions on how to pull the data locally in our Examples folder. We encourage all users to review [Yelp Dataset: Terms of Service](https://terms.yelp.com/tos/en_us/20200101_en_us/) and [Nutritionix Dataset: Terms and Conditions](https://www.nutritionix.com/apiterms) for more information.


<h2>Organization of the Project</h2>
The project has the following structure (8 directories, 36 files): <br>

```
  
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
    │   │   └── download_nutritionix_data.py
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

<h2>Installation and Running Tests</h2> 
First, you will need to clone this repository:  
```git clone https://github.com/nhalfi/Yelp_Recommendations.git```  

Next, navigate to the Yelp_Recommendations directory and run the setup.py script, which installs prerequisite packages:  
```cd Yelp_Recommendations ```    
```python setup.py install ```    

To execute our unit tests, navigate to our tests folder and run the following:  
``` cd Yelp/tests```  
``` python test_download_nutritionix_data.py```  
``` python test_data_processing.py```  
``` python test_text_classification.py```  
``` python test_restaurants_dao.py```  



<h2>Examples (How to use Yelp-Recommendations)</h2> 

To better understand how to use ```Yelp-Recommendations``` , please refer to the [usage examples](https://github.com/nhalfi/Yelp_Recommendations/tree/main/examples) provided in this repository, which will help with the following:

  * Launching and Interacting with the App <br>
  * Reproducing our Model
    * Download Extracted Yelp JSON Files
    * Download Nutritionix Data
    * Process the Datasets and Run the Text Classification Model

<h2>Limitations and Future Work</h2> 

  * We were limited to specific cities included in the Yelp dataset <br>
  * We would like to explore additional training datasets that are more similar to Yelp's data <br>
  * We would like to leverage the photos in the Yelp dataset to perform image classification to determine health scores, in addition to text classification <br>

<h2>Acknowledgements</h2> 

We are grateful to our course instructors, Mark Friedman and Bernease Herman, for their valuable guidance on our DATA 515 project, which improved our understanding of software design best practices. <br>
<br>



