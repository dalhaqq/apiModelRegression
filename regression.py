import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import warnings # supress warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('./new-dataset.csv')

df = df.drop_duplicates(keep='first')

x = df.drop(columns=['is_color','bw_area','price'])
y = df['price']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=4)

lin_reg = LinearRegression()
lin_reg.fit(x_train, y_train)

def pricePrediction(color_area, print_area):
    prediction = lin_reg.predict([[color_area, print_area]])
    if prediction[0] < 300 and color_area == 0 :
        prediction[0] = 300
    if prediction[0] < 500 and color_area != 0 :
        prediction[0] = 500
    return (round(prediction[0]))