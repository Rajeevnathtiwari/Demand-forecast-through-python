

import csv
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
import plotly.express as px
def details():
    company_name = input("Enter your Company name: ")
    password = input("Enter your password: ")

    print("Please wait processing ..")
    time.sleep(5)  # Delay for 5 seconds

    print("Thank you for waiting")

    with open("company_info.txt", "a") as file:
        file.write(f"Company Name: {company_name}\n")
        file.write(f"Password: {password}\n\n")

    print("Company information has been saved to 'company_info.txt'.")

    print("Please wait processing ..")
    time.sleep(5)

def arima_forecast(units_sold, date, category, X_test, y_test,z_test):
    try:
        # Create a DataFrame with units sold and date
        data = pd.DataFrame({'UnitsSOLD': units_sold, 'Date': date,'CategoryName':category})
        print(data)

        # Fit ARIMA model
        model = ARIMA(units_sold , order=(2, 2, 2))  # Example order, you may need to tune this
        result = model.fit()

        # Forecast future demand
        forecast_steps = len(X_test)  # Example number of steps to forecast
        forecast = result.get_forecast(steps=forecast_steps)

        # Get forecasted values
        forecast_values = forecast.predicted_mean.tolist()# pridicted upcoming unitssold for the future



        # Create a line graph using Seaborn
        sns.lineplot(x=X_test, y= forecast_values)
        sns.set_theme(style="darkgrid")  # Set a theme for better aesthetics
        sns.despine()  #  Remove top and right spines for a cleaner look
        plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for readability
        plt.title("Units Sold vs Date")
        plt.xlabel("Date")
        plt.ylabel("Forecasted Units Sold")
        data1 = pd.DataFrame({'Date': X_test, 'CategoryName':z_test})
        data1['ForecastedUnitsSold'] = forecast_values

    # creating treemap

        fig = px.treemap(data1, path=['CategoryName'], values='ForecastedUnitsSold',hover_data=['ForecastedUnitsSold'], custom_data=['ForecastedUnitsSold'])

        fig.update_layout(title='DEMAND FORECAST FOR CATEGORY')
        # Creating bar graph
        plt.figure(figsize=(100, 60))
        plt.bar(data1['ForecastedUnitsSold'],data1['CategoryName'])
        plt.xlabel('CategoryName')
        plt.ylabel('Forecasted Units Sold')
        plt.title('Forecasted Units Sold by Category')

        fig.show()
        plt.show()

        # Save forecasted data to CSV
        save_to_csv("C:\\Users\\rajee\\OneDrive\\Desktop\\arima_forecast.csv", X_test, data1['ForecastedUnitsSold'],z_test)
    except Exception as e1:
        print("Error occured :",e1)


def save_to_csv(file_path,  date,unitssold,categoryname):
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date ", "UnitsSold","CategoryName"])
        writer.writerows(zip(date, unitssold,categoryname))

    print("Forecasted data saved to", file_path)

def main():
    details()
    try:
        file_path = "E:\\PROJECTS\\MINOR 1\\sample2.csv"

        # Use pd.read_csv to read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Print the column names to identify the correct column names
        try:
            print(df.columns)
        except Exception as e1:
            print('Printing column names error:', e1)

        # Split the data into training and test sets (80% training, 20% test)
        df['Date'] = pd.to_datetime(df['Date'])

        X = df['Date']
        Y = df['units_sold']
        Z= df['categoryname']
        X_train, X_test, y_train, y_test,z_train ,z_test = train_test_split(X, Y,Z, test_size=0.2, random_state=42)
        arima_forecast(y_train, X_train,z_train, X_test, y_test,z_test)
    except Exception as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    main()