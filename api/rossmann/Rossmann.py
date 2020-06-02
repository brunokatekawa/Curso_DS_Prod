import pickle
import inflection
import pandas as pd
import numpy as np
import math
import datetime

class Rossmann(object):
    def __init__(self):
        self.home_path = '/Users/brunokatekawa/Desktop/Data Science/DataScienceProducao/Curso_DS_Prod/'
        # loads the rescaling
        self.competition_distance_scaler   = pickle.load(open(self.home_path + 'parameter/competition_distance_scaler.pkl', 'rb'))
        self.competition_time_month_scaler = pickle.load(open(self.home_path + 'parameter/competition_time_month_scaler.pkl', 'rb'))
        self.promo_time_week_scaler        = pickle.load(open(self.home_path + 'parameter/promo_time_week_scaler.pkl', 'rb'))
        self.year_scaler                   = pickle.load(open(self.home_path + 'parameter/year_scaler.pkl', 'rb'))
        
        # loads the encoder
        self.store_type_scaler             = pickle.load(open(self.home_path + 'parameter/store_type_scaler.pkl', 'rb'))

        
    def data_cleaning(self, df1):

        ## 1.1. Renaming columns
        # stores the old column names
        cols_old = ['Store', 'DayOfWeek', 'Date', 'Open', 'Promo', 'StateHoliday', 
                    'SchoolHoliday', 'StoreType', 'Assortment','CompetitionDistance', 'CompetitionOpenSinceMonth', 
                    'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval']

        # snake_case
        snakecase = lambda x: inflection.underscore(x)

        # creates new columns from old columns in snakecase 
        cols_new = list(map(snakecase, cols_old))

        # renames the old columns
        df1.columns = cols_new


        ## 1.3.  Checking data types
        # transforms 'date' column to datetime type
        df1['date'] = pd.to_datetime(df1['date'])


        ## 1.5.  Filling out the NaN values
        ### 1.5.1 Filling the competition data

        # competition_distance
        # let's assume that the distance from competitors is so long that there are no competitors
        # applies for each column record: competition_distance
        #     assign 200000.0 if record == NaN ; assign its current value if record != NaN
        df1['competition_distance'] = df1['competition_distance'].apply(lambda x: 200000.0 if math.isnan(x) else x)

        # competition_open_since_month
        # let's assume that the opening date is the store sales date: date
        # axis=1 -> apply in the row along the columns, because we have more than one column in the expression
        df1['competition_open_since_month'] = df1.apply(lambda x: x['date'].month if math.isnan(x['competition_open_since_month']) else x['competition_open_since_month'], axis=1)

        # competition_open_since_year 
        df1['competition_open_since_year'] = df1.apply(lambda x: x['date'].year if math.isnan(x['competition_open_since_year']) else x['competition_open_since_year'], axis=1)


        ### 1.5.2 Filling the promotion data
        # promo2_since_week
        df1['promo2_since_week'] = df1.apply(lambda x: x['date'].week if math.isnan(x['promo2_since_week']) else x['promo2_since_week'], axis=1)

        # promo2_since_year
        df1['promo2_since_year'] = df1.apply(lambda x: x['date'].year if math.isnan(x['promo2_since_year']) else x['promo2_since_year'], axis=1)

        # promo_interval
        # creates a dictionary that will help in mapping
        month_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                     7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        # fills in the NaN with zeroes
        df1['promo_interval'].fillna(0, inplace=True)

        # creates the 'month_map' column as the month mapping of the 'date' column
        df1['month_map'] = df1['date'].dt.month.map(month_map)


        # make a split in 'promo_interval' column and creates a list containing the values
        # check if the value of 'month_map' is within that list
        # creates column 'is_promo' with numeric values (1 = was in promo or 0 = was not in promo) based on the verification
        df1['is_promo'] = df1[['promo_interval','month_map']].apply(lambda x: 0 if x['promo_interval'] == 0 else 1 if x['month_map'] in x['promo_interval'].split(',') else 0, axis=1)


        ## 1.6.  Changing data types
        # transforms competition data to int
        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype(int)
        df1['competition_open_since_year'] = df1['competition_open_since_year'].astype(int)

        # transforms promotion data to int
        df1['promo2_since_week'] = df1['promo2_since_week'].astype(int)
        df1['promo2_since_year'] = df1['promo2_since_year'].astype(int)
        
        return df1

    
    def feature_engineering(self, df2):
        # 2.0 FEATURE ENGINEERING
        ## 2.4 Feature engineering - de facto

        # year
        df2['year'] = df2['date'].dt.year

        # month
        df2['month'] = df2['date'].dt.month

        # day
        df2['day'] = df2['date'].dt.day

        # week of year
        df2['week_of_year'] = df2['date'].dt.weekofyear

        # year week
        df2['year_week'] = df2['date'].dt.strftime('%Y-%W')


        # competition since
        # creates a new datetime column 'competition_since' which is a compound of two columns
        # we are specifying that it will always have the 1st day of the month
        df2['competition_since'] = df2.apply(lambda x: 
                                             datetime.datetime(year=x['competition_open_since_year'], 
                                                                         month=x['competition_open_since_month'], 
                                                                         day=1), 
                                             axis=1)


        # How many months has passed since the competition store opened?
        # gets the difference between columns and divides it by 30 to make the monthly granularity
        #     then we get the days as int type
        df2['competition_time_month'] = ((df2['date'] - df2['competition_since']) / 30).apply(lambda x: x.days).astype(int)


        # promo since
        df2['promo_since'] = df2['promo2_since_year'].astype(str) + '-' +df2['promo2_since_week'].astype(str)

        # converts values from 'promo_since' to datetime considering 7 days
        df2['promo_since'] = df2['promo_since'].apply(lambda x: 
                                 datetime.datetime.strptime(x + '-1', '%Y-%W-%w') - datetime.timedelta(days=7))

        # How many weeks has passed since the promotion started?
        # OR for how long (in weeks) the promotion is active?
        # gets the difference between columns and divides it by 7 to make the weekly granularity
        #     then we get the days as int type
        df2['promo_time_week'] = ((df2['date'] - df2['promo_since']) / 7).apply(lambda x: x.days).astype(int)


        # assortment
        # replaces the values to make easier to understand them
        df2['assortment'] = df2['assortment'].apply(lambda x: 'basic' if x == 'a' else 'extra' if x == 'b' else 'extended')

        # state holiday
        # replaces the values to make easier to understand them
        df2['state_holiday'] = df2['state_holiday'].apply(lambda x: 'public_holiday' if x == 'a' else 'easter_holiday' if x == 'b' else 'christmas' if x == 'c' else 'regular_day')


        # 3.0 VARIABLE FILTERING
        ## 3.1 Row filtering
        # gets only the rows for open stores
        df2 = df2[df2['open'] != 0]
        
        ## 3.2 Column filtering
        # drops the columns
        cols_drop = ['open', 'promo_interval', 'month_map']
        df2 = df2.drop(cols_drop, axis=1)
        
        return df2


    def data_preparation(self, df5):
        
        ## 5.2 Rescaling
        ### 5.2.1 Rescaling competition_distance
        # competition_distance
        df5['competition_distance'] = self.competition_distance_scaler.fit_transform(df5[['competition_distance']])


        ### 5.2.2 Rescaling competition_time_month
        # competition_time_month
        df5['competition_time_month'] = self.competition_time_month_scaler.fit_transform(df5[['competition_time_month']])

        
        ### 5.2.3 Rescaling promo_time_week
        # promo_time_week
        df5['promo_time_week'] = self.promo_time_week_scaler.fit_transform(df5[['promo_time_week']])

        # year
        df5['year'] = self.year_scaler.fit_transform(df5[['year']])
        
        
        ## 5.3 Transformation
        ### 5.3.1 Encoding
        #### 5.3.1.1 One Hot Encoding for state_holiday

        # state_holiday
        # One Hot Encoding
        df5 = pd.get_dummies(df5, prefix=['state_holiday'], columns=['state_holiday'])


        #### 5.3.1.2 Label Encoding for store_type
        # store_type
        # Label Encoding - as we don't know if there is an order
        df5['store_type'] = self.store_type_scaler.fit_transform(df5['store_type'])


        #### 5.3.1.3 Label Encoding for assortment
        # assortment
        # Ordinal Encoding - as there is an order

        # explicitly dictates the encoding codes
        assortment_dict = {'basic':1, 'extra': 2, 'extended': 3}

        # maps the names
        df5['assortment'] = df5['assortment'].map(assortment_dict)


        ### 5.3.2 Nature Transformation
        # day_of_week
        df5['day_of_week_sin'] = df5['day_of_week'].apply(lambda x: np.sin(x *(2. * np.pi / 7)))
        df5['day_of_week_cos'] = df5['day_of_week'].apply(lambda x: np.cos(x *(2. * np.pi / 7)))

        # month
        df5['month_sin'] = df5['month'].apply(lambda x: np.sin(x *(2. * np.pi / 12)))
        df5['month_cos'] = df5['month'].apply(lambda x: np.cos(x *(2. * np.pi / 12)))

        # day
        df5['day_sin'] = df5['day'].apply(lambda x: np.sin(x *(2. * np.pi / 30)))
        df5['day_cos'] = df5['day'].apply(lambda x: np.cos(x *(2. * np.pi / 30)))

        # week_of_year
        df5['week_of_year_sin'] = df5['week_of_year'].apply(lambda x: np.sin(x *(2. * np.pi / 52)))
        df5['week_of_year_cos'] = df5['week_of_year'].apply(lambda x: np.cos(x *(2. * np.pi / 52)))
        
        cols_selected = ['store', 'promo', 'store_type',
                       'assortment','competition_distance', 'competition_open_since_month',
                       'competition_open_since_year','promo2', 'promo2_since_week',
                       'promo2_since_year','competition_time_month', 'promo_time_week',
                       'day_of_week_sin','day_of_week_cos', 'month_sin','month_cos',
                       'day_sin','day_cos', 'week_of_year_sin', 'week_of_year_cos']
        
        return df5[cols_selected]
    
    
    def get_prediction(self, model, original_data, test_data):
        #predicts
        pred = model.predict(test_data)
        
        # joins pred into the original data
        original_data['prediction'] = np.expm1(pred)
        
        return original_data.to_json(orient='records', date_format='iso')