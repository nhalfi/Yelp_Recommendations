#  import module and libraries
import sys
sys.path.append('../')
from text_classification import text_classification as tc  # noqa: E402
# ignoring E402 because need import sys and sys.path to access submodule
import pandas as pd  # noqa: E402
import unittest  # noqa: E402
from sklearn.feature_extraction.text import CountVectorizer  # noqa: E402
from sklearn.naive_bayes import MultinomialNB  # noqa: E402


class MyTestClassification(unittest.TestCase):
    def setup(self):
        print('START Test ...')
    # ...............................................................................................

    def test_split_test_train_dataset(self):
        """
            Test the split_test_train_dataset function
            - Call the function and validate the return value from the function
            - If the function is working correctly, it will return the
                sub-datasets
            - The sub datasets size will be greater than 0
            - If the sub datasets are 0 (aka. empty), and exception is raise
                 to fail the test
        """
        print('START Testing.....')
        print()

        value_x_train = 0
        value_x_test = 0
        value_yelp_test = 0

        res_health = pd.read_csv("sample_nutritionix_data.csv")
        yelp = pd.read_csv("sample_yelp_data.csv")

        value_x_train, value_x_test, value_yelp_test = \
            tc.split_test_train_dataset(res_health, yelp)

        print('Total records of x_train: ', value_x_train.count()[0])
        print('Total records of x_test: ', value_x_test.count()[0])
        print('Total records of yelp_test: ', value_yelp_test.count()[0])

        self.assertGreater(value_x_train.count()[0], 0,
                           'Fail: x_train sub-dataset')
        self.assertGreater(value_x_test.count()[0], 0,
                           'Fail: x_test sub-dataset')
        self.assertGreater(value_yelp_test.count()[0], 0,
                           'Fail: yelp_test sub-dataset')

        print('END Testing.....')
        print()

    # ...............................................................................................
    def test_vectorize_text(self):
        """
        Test the vectorize_text function
        - Function to invoke the CountVectorize from the library to vectorize
            data for model
        - Return the vecterization data for transformation for training, test
             and yelp data
        - An exception will raise when the output is not in a vector format
        """

        print('START Testing.....')
        print()

        data_1 = {'filtered_caption': ['apple is healthy and delicious']}
        data_2 = {'filtered_caption': ['apple']}
        data_3 = {'filtered_caption': ['healthy']}

        df_1 = pd.DataFrame(data_1, columns=['filtered_caption'])
        df_2 = pd.DataFrame(data_2, columns=['filtered_caption'])
        df_3 = pd.DataFrame(data_3, columns=['filtered_caption'])

        check_train, check_test, check_yelp = \
            tc.vectorize_text(df_1, df_2, df_3)

        """
        data_1 has 5 words, so the vectorize value will be a matrix of
        5 elements. Because we vectorize (fit) x_train and we use that
        vector to transform the x_test and yelp_test. Therefore, the matrixes
        of x_test and yelp_test will have the same size of 5,
        even though data_2 and data_3 have only one word
        """

        print(check_train.shape)
        print(check_test.shape)
        print(check_yelp.shape)

        # we know that vectorize library will arrange the word in alphabetical
        # order from left to right
        # data_1 order will be [and, apple, delicious, healthy, is]
        # data_1 vectorizes be [ 1 ,   1  ,    1     ,    1   ,  1]
        # data_2 vectorizes be [ 0 ,   1  ,    0     ,    0   ,  0]
        # data_3 vectorizes be [ 0,    0  ,    0     ,    1   ,  0]

        # matrix index position  0.....1.......2..........3......4

        # We can validate the same "apple" in data_2 will be in the same index
        # position of "apple" in data_1
        print('Matrix index of apple value:', check_test.toarray()[0][1])
        self.assertEqual(check_test.toarray()[0][1], 1, 'Fail: x_test has \
            different vectorized matrix index')

        # We can validate the dame "healthy" in data_3 will be in the same
        # index position of "healthy" in data_1
        print('Matrix index of healthy value: ', check_yelp.toarray()[0][3])
        self.assertEqual(check_yelp.toarray()[0][3], 1, 'Fail: yelp_test has \
            different vectorized matrix index')

        print('END Testing.....')
        print()

    # ...............................................................................................

    def test_fit_and_evaluate_model(self):
        """
        Test the fit_and_evaluate_model function
        - This function takes in the vecterized values and perform fit
            then evaluate model
        - It returns a confusion matrix, accuracy, and model
        - An exception will raise when it fails the model
        """

        data1 = [['salad and greens', 1], ['apple', 1], ['saute veggie', 1],
                 ['chicken wings', 0], ['fried french fries', 0],
                 ['Beef Burger', 0], ['lamb burger', 0]]
        data1 = pd.DataFrame(data1, columns=['caption', 'healthy'])
        # Create the pandas DataFrame
        data2 = [['greens', 1], ['salad', 1], ['veggie', 1], ['butter', 0],
                 ['chocolate', 0], ['french fries', 0], ['Burger', 0]]
        data2 = pd.DataFrame(data1, columns=['caption', 'healthy'])
        label_col = data1['healthy']

        vector = CountVectorizer()
        vector.fit(data1["caption"])
        vector = CountVectorizer(vocabulary=vector.vocabulary_)
        # vocabulary is a parameter, it should be vocabulary_
        # as it is an attribute.
        training_data = vector.transform(data1["caption"])
        test_data = vector.transform(data2["caption"])

        check_conf_matrix, check_accuracy, check_model = \
            tc.fit_and_evaluate_model(training_data, test_data,
                                      data2, label_col)

        print('Dimension of confusion Matrix:', check_conf_matrix.ndim)
        self.assertEqual(check_conf_matrix.ndim, 2, 'Fail: check_conf_matrix \
                         has different dimension')

        # We can validate the dame "healthy" in data_3 will be in the same
        #  index position of "healthy" in data_1
        print('Model Accuracy: ', check_accuracy)
        self.assertEqual(isinstance(check_accuracy, float), True, 'Fail: Model \
                        accuracy out of bounds')

        # We can validate the dame "healthy" in data_3 will be in the same
        # index position of "healthy" in data_1
        print('Model results empty: ', (check_model == ""))
        self.assertNotEqual(check_model, "", 'Fail: Model not generated')

        print('END Testing.....')
        print()

    # ...............................................................................................

    def test_predict_on_Yelp(self):
        """
            Test the prediction model
            - The function will predict the model with Naive Bayes classifier
            - An exception will raise if the final result is not
                correctly processed
        """

        data1 = [['salad and greens', 1], ['apple', 1], ['saute veggie', 1],
                 ['chicken wings', 0], ['fried french fries', 0],
                 ['Beef Burger', 0], ['lamb burger', 0]]
        data1 = pd.DataFrame(data1, columns=['caption', 'healthy'])
        label_col = data1['healthy']
        data2 = ['Fries', 'salad']
        data2 = pd.DataFrame(data2, columns=['caption'])

        yelp = [['K_9pvEE-fJQyYExAGe0X0g', 'burger', 'food',
                'Texas Land & Cattle', '7779 Lyles Ln', 'Concord',
                 'NC', '28027', '35.3654956', '-80.7120321', '3', '145',
                 'Comfort Food'],
                ['K_xAGerhgkueX0g', 'Salad', 'food', 'LA health',
                '1234 Hollywood Ln', 'valley', 'LA', '28057',
                    '35.3655746', '-80.71221', '2', '13', 'fast Food']]
        yelp = pd.DataFrame(yelp, columns=['business_id', 'caption',
                            'label', 'name', 'address', 'city', 'state',
                                           'postal_code', 'latitude',
                                           'longitude', 'stars',
                                           'review_count', 'categories'])

        vector = CountVectorizer()
        vector.fit(data1["caption"])
        vector = CountVectorizer(vocabulary=vector.vocabulary_)
        # vocabulary is a parameter, it should be vocabulary_ as
        # it is an attribute.

        training_data = vector.transform(data1["caption"])
        test_data = vector.transform(data2["caption"])

        model = MultinomialNB().fit(training_data, label_col)

        Check_yelp_final = tc.predict_on_Yelp(model, test_data, yelp)

        print('Dimension of Final Yelp dataset:', Check_yelp_final.ndim)
        self.assertEqual(Check_yelp_final.ndim, 2, 'Fail: Yelp dataset with \
            predictions not generated')


if __name__ == '__main__':
    unittest.main()
