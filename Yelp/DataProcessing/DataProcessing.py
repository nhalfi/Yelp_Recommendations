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

def textProcess(df, token_col,output_name):
    """
    -function to perform text preprocessing activities needed for text classification
    -df: input dataframe that contains text to be preprocessed
    -token_col: column name with relevant words to tokenize, filter, and stem
    -output_name: base name for file output
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

    #export to csv
    file_name = str(output_name+'_tokenized.csv')
    print(file_name)
    file_path = str('../Data/'+file_name)
    print(file_path)
    df2.to_csv(file_path)

            

def main():
    #convert JSON files to Pandas dataframes
    #due to GitHub file size constraints, these files must be downloaded locally; see instructions in README
    df_business = pd.read_json('../Data/yelp_academic_dataset_business.json',lines=True) 
    df_photos = pd.read_json("../Data/photos.json", lines=True)

    #### restaurant filtering ####

    df_business['restaurant'] = df_business['categories'].str.contains('Restaurants|Food') 
    df_restaurants = df_business[df_business['restaurant']==True]

    #drop unneeded columns and output to csv
    df_restaurants = df_restaurants.drop(['is_open','attributes','hours','restaurant'],axis = 1)
    df_restaurants.to_csv('../Data/yelp_business_clean.csv')

    #### photo filtering ####
    df_photos = df_photos[df_photos['business_id'].isin(df_restaurants['business_id'])]
    df_photos = df_photos[df_photos['label']=="food"]
    df_photos = df_photos[df_photos['caption']!=""] # exclude records with blank captions
    #output to csv
    df_photos.to_csv('../Data/yelp_photos_clean.csv')

    #join dataframes on business_id
    df_join = df_photos.merge(df_restaurants,how='inner')
    df_join.to_csv('../Data/yelp_joined_clean.csv')

    #preprocess joined dataset
    textProcess(df_join, 'caption','yelp_final')
    

    #load training data from Nutritionix API
    #this dataset was extracted via a PowerShell script; see DownloadNutritionixData.ps1 in the DataProcessing folder and the README instructions
    with open('../Data/restaurants_items.json','r') as f:
        data=f.read()
    obj = json.loads(data)
    df_nutritionix = pd.DataFrame.from_dict(obj, orient='columns')

    FIELDS = ["fields.item_name","fileds.brand_name","fields.upc","fields.nt_ingredient_statement","fields.nf_calories", "fields.nf_calories_from_fat","fields.nf_total_fat","fields.nf_saturated_fat","fields.nf_trans_fatty_acid","fields.nf_cholesterol","fields.nf_sodium","fields.nf_sugars","fields.nf_protein","fields.nf_serving_per_container"]
    df_nutritionix = pd.json_normalize(obj)

    df_nutritionix_health = df_nutritionix.copy()
    conditions = [
        (df_nutritionix_health['fields.nf_calories'] >500)|(df_nutritionix_health['fields.nf_calories_from_fat'] > 200)|(df_nutritionix_health['fields.nf_total_fat']> 20) | (df_nutritionix_health['fields.nf_saturated_fat'] > 8) | (df_nutritionix_health['fields.nf_trans_fatty_acid'] >0) | (df_nutritionix_health['fields.nf_cholesterol'] > 100) | (df_nutritionix_health['fields.nf_sodium']> 766) | (df_nutritionix_health['fields.nf_sugars']> 30)]
    choices = [0]
    df_nutritionix_health['healthy'] = np.select(conditions, choices, default=1)
    df_nutritionix_health.to_csv('../Data/nutritionix_health.csv', index=False)


    #preprocess training dataset
    textProcess(df_nutritionix_health, 'fields.item_name','nutritionix')

if __name__ == "__main__":
    main()