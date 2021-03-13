#script to download data from Nutritionix API
#after running, add [ to the beginning of the output JSON file, and replace the final , with a ]

for ($i = 0; $i -le 3000; $i = $i + 50)
{
	$query = '{\"appId\":\"91e4a07d\", \"appKey\":\"03d1f9a480f0ee71eb064d5d6fa7264e\", \"fields\":[\"item_name\",\"brand_name\",\"upc\",\"nt_ingredient_statement\",\"nf_calories\", \"nf_calories_from_fat\",\"nf_total_fat\",\"nf_saturated_fat\",\"nf_trans_fatty_acid\",\"nf_cholesterol\",\"nf_sodium\",\"nf_sugars\",\"nf_protein\",\"nf_serving_per_container\"],\"limit\":50, \"offset\":' + $i + ',\"filters\":{\"item_type\":1}}';

	$curr = curl -X POST https://api.nutritionix.com/v1_1/search -H 'Content-Type: application/json' -d $query | ConvertFrom-Json
	$str = $curr.hits | convertto-json
	$str = $str.Replace('[','').Replace(']','')
	$str + ',' >> restaurants_items.json
}
