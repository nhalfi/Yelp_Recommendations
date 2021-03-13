## How to Use Yelp_Recommendations

### Launching the App

To launch the app, run the following commands in the terminal:


You should now see the following UI:


You can interact with the app throught the following actions:


### Reproducing our Model

The data we used to train our model and generate predictions comes from a static datasource, and the final model results are stored in this repository. Therefore, there is no need to rerun the logic found in the data_processing and text_classification modules. However, if you would like to do so for your own interest, the steps are as follows.

#### 1. Download Extracted Yelp JSON Files

Download the following files and copy them to the data folder (the file sizes were too large to store directly in GitHub). Make sure to not change the file names.
* [yelp_academic_dataset.json](https://drive.google.com/file/d/1yKgjuFgYcLCfU2guLJjzCNnAVSnD_D5s/view?usp=sharing)
* [photos.json](https://drive.google.com/file/d/1iei3dhkCGLLgra_Eq1OqQX2DW2dFfQa7/view?usp=sharing)

We extracted these files from the Yelp Open Dataset. For more information and additional data, please visit this [link](https://www.yelp.com/dataset).

#### 2. Download Nutritionix Data

We have already extracted this dataset for you in the data folder (restaurants_items.json). However, if you would like to pull from the Nutritionix API yourself, proceed with the following:

Navigate to the data folder:   
```cd Yelp/data```  
Run the download_nutritionix_data.ps1 script:  
``` powershell.exe -file "download_nutritionix_data.ps1"```

You should now see the restaurants_items.json file. Open the file and add an opening bracket at the beginning, ```[```, and replace the final ```,``` with a closing bracket, ```]```. Move the saved restaurants_items.json file to the data folder.  
Please refer to the following [link](https://www.nutritionix.com/business/api) for more information on the Nutritionix API.

#### 3. Process the Datasets and Run the Text Classification Model

Now that we have pulled the necessary data files, we can run the data_processing module, which cleans the Yelp and Nutritonix datasets and performs text pre-processing that prepares the data to be ingested by our machine learning model. 

Navigate to the data_processing folder and run data_processing.py :   
```cd ../data_procesing```  
```python data_processing.py```

Next, navigate to the text_classification folder and run text_classification.py :  
```cd ../text_classification```  
```python text_classification.py```

Now, the final health scores have been generated for each restaurant in the Yelp_Healthy_restaurant_predictions.csv file in the data folder (this is the data that the app consumes and exposes).
