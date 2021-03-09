# Module: DataPreprocessing.py
# Purpose: clean, transform, and prepare data for modeling

#import libraries
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import numpy as np
import json
import pandas as pd

class ProcessingError(Exception):
    #raised if output from text_process produces an empty dataframe
    pass

def text_process(df, token_col):
    """
    -function to perform text preprocessing activities needed for text classification
    -df: input dataframe that contains text to be preprocessed
    -token_col: column name with relevant words to tokenize, filter, and stem
    -returns dataframe with text that has been tokenized, filtered for stopwords, and stemmed
    """

    #create dataframe copy
    df2 = df.copy()
    #create separate column for tokenized caption
    df2['caption_clean'] = df2[token_col]
    df2['caption_clean'] = df2['caption_clean'].replace('[^a-zA-Z0-9 ]', '', regex=True)
    df2['caption_clean'] = df2['caption_clean'].str.lower()
    df2['caption_clean'] = df2.apply(lambda row: nltk.word_tokenize(row['caption_clean']), axis=1)

    #filter out stopwords
    stop_words = stopwords.words('english')
    df2['filtered_caption'] = df2['caption_clean']
    df2['filtered_caption']=df2['filtered_caption'].apply(lambda x:[item for item in x if item not in stop_words])

    #perform stemming to get stems of words
    porter = PorterStemmer()
    df2['filtered_caption'] = df2['filtered_caption'].apply(lambda x:[porter.stem(item) for item in x])

    if(len(df2)==0):
        raise ProcessingError(("ProcessingError: tokenized dataframe contains no records"))
    else:
        #return tokenized dataframe
        return(df2)
            
def calculate_health(df):
    """
    -function that contains logic to calculate healthy boolean flag for training data
    -df: input dataframe that contains restaurant menu items and nutritional information
    -returns dataframe with calculated healthy column
    """
    
    df2 = df.copy()
    conditions = [(df2['fields.nf_calories'] >500)|(df2['fields.nf_calories_from_fat'] > 200)|(df2['fields.nf_total_fat']> 20) 
    | (df2['fields.nf_saturated_fat'] > 8) | (df2['fields.nf_trans_fatty_acid'] >0) | (df2['fields.nf_cholesterol'] > 100) 
    | (df2['fields.nf_sodium']> 766) | (df2['fields.nf_sugars']> 30)]
    choices = [0]
    df2['healthy'] = np.select(conditions, choices, default=1)

    return(df2)

def clean_yelp(df_business, df_photos):
    """
    -function that contains logic filter and join yelp datasets
    -df_business: input dataframe that contains Yelp business data
    -df_photos: input dataframe that contains Yelp photo data
    -returns cleaned and joined dataframe
    """
    
    df_business['restaurant'] = df_business['categories'].str.contains('Restaurants|Food') 
    df_restaurants = df_business[df_business['restaurant']==True]

    #drop unneeded columns and output to csv
    df_restaurants = df_restaurants.drop(['is_open','attributes','hours','restaurant'],axis = 1)
    #df_restaurants.to_csv('../data/yelp_business_clean.csv')

    #### photo filtering ####
    df_photos = df_photos[df_photos['business_id'].isin(df_restaurants['business_id'])]
    df_photos = df_photos[df_photos['label']=="food"]
    df_photos = df_photos[df_photos['caption']!=""] # exclude records with blank captions
    #output to csv
    #df_photos.to_csv('../data/yelp_photos_clean.csv')

    #join dataframes on business_id
    df_join = df_photos.merge(df_restaurants,how='inner')

    return(df_join)

def main():
    #convert JSON files to Pandas dataframes
    #due to GitHub file size constraints, these files must be downloaded locally; see instructions in README
    try:
        df_business = pd.read_json('../data/yelp_academic_dataset_business.json',lines=True) 
        df_photos = pd.read_json("../data/photos.json", lines=True)
    except Exception:
        print("Please double check that you have locally downloaded the Yelp Academic dataset (see README for details).")

    #filter and join data
    df_join = clean_yelp(df_business,df_photos)
    df_join.to_csv('../data/yelp_joined_clean.csv')

    #preprocess joined dataset
    df_yelp_tokenized = text_process(df_join, 'caption')
    #output to csv
    df_yelp_tokenized.to_csv('../data/yelp_final_tokenized.csv')
    
    #load training data from Nutritionix API
    #this dataset was extracted via a PowerShell script; see DownloadNutritionixData.ps1 in the DataProcessing folder and the README instructions
    try:
        with open('../data/restaurants_items.json','r') as f:
            data=f.read()
    except Exception:
        print("Please double check that you have locally downloaded the Nutritionix dataset (see README for details).")

    obj = json.loads(data)
    df_nutritionix = pd.DataFrame.from_dict(obj, orient='columns')
    df_nutritionix = pd.json_normalize(obj)

    df_nutritionix_health = calculate_health(df_nutritionix)
    df_nutritionix_health.to_csv('../data/nutritionix_health.csv', index=False)

    #preprocess training dataset
    df_nutritionix_tokenized = text_process(df_nutritionix_health, 'fields.item_name')
    df_nutritionix_tokenized.to_csv('../data/nutritionix_tokenized.csv')

if __name__ == "__main__":
    main()