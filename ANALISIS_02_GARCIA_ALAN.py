"""
Alan Garcia
February 2022
Synergy Logistics Data
"""

#All the necessary libraries are imported: pandas, seaborn and matplotlib
from operator import index
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#The main dataframe is imported from an external file
df = pd.read_csv("synergy_logistics_database.csv", index_col="register_id")

colorsPie = sns.color_palette('pastel')#sets the colors that will be used for the pie charts 

#----------------------CREATING DATAFRAMES FROM MAIN DATAFRAME----------------------#

routes = df[["direction", "origin", "destination", "transport_mode", "total_value"]]#new dataframe with the columns we need

routes["trips"] = 1 #creates a new column that will be useful for counting the number of trips

def route_Path(row): #a function to determine the path based on: origin, destination and transport mode
    result = row["origin"] + "/" + row["destination"] + "/" + row["transport_mode"]
    return result

routes["route"] = routes.apply(route_Path, axis = 1) #creates a new column including the full path
route_value = routes[["direction", "route", "total_value", "trips"]] #new dataframe with necessary columns
route_value = route_value.groupby("route").sum() #we group the dataframe by path taken and sum all values for each path
totalValue = df["total_value"].sum() #variable containing the total value from all imports and exports

transportMode = df[["transport_mode", "total_value"]]
transports = transportMode.groupby("transport_mode").sum() #new dataframe where we sum all values for each transport mode

def country_of_value(row): #function to determine which country generates the value, origin for exports and destination for imports
    if row["direction"] == "Exports":
        result = row["origin"]
    elif row["direction"] == "Imports":
        result = row["destination"]
    return result

def percentage(row): #funtion to obtain total value per row in terms of a percentage
    result = row["total_value"] * 100 / totalValue
    return result

countries = df[["direction", "total_value"]]
countries["countries_of_value"] = df.apply(country_of_value, axis = 1) #a new column with the country that generates the value is added
countriesOfValue = countries.groupby("countries_of_value").sum() #new dataframe grouping and adding all values based on the country of value
countriesOfValue["percentage"] = countriesOfValue.apply(percentage, axis = 1) #new column containing value in terms of percentage

#---------------------FUNCTIONS----------------------#

def topRoutesByTrips(): # Function to obtain the top routes by number of trips
    route_value.sort_values(by=["trips"], inplace=True, ascending=False) #sort the dataframe by number of trips
    route_value.to_csv("topRoutesByTrips.csv") #save dataframe to an external file
    print("The top ten routes by total trips are:\n")
    print(route_value.head(10))
    topTenTotalValue = route_value["total_value"].head(10).sum()
    print(f"Overall total value: {totalValue}")
    print(f"Value of top 10 routes by trips: {topTenTotalValue}")
    tripsPercentage = topTenTotalValue * 100 / totalValue
    print(f"Percentage: {tripsPercentage}%")
    print("For more information check the generated topRoutesByTrips.csv file")
    data = [tripsPercentage, 100 - tripsPercentage] #data for pie chart
    labels = ["top 10 routes\nper trips value", "remaining value"] #labels for pie chart
    sns.barplot(data = route_value.reset_index().head(10), x = "trips", y = "route") #displays top 10 routes by number of trips
    plt.show()
    plt.pie(data, labels = labels, colors = colorsPie, autopct='%.0f%%') #displays pie chart comparing the value of the top routes compared to total value
    plt.show()

def topRoutesByValue(): # Function to obtain the top routes by value
    route_value.sort_values(by=["total_value"], inplace=True, ascending=False)#sort the dataframe by value
    route_value.to_csv("topRoutesByValue.csv")#save dataframe to an external file
    print("The top ten routes by total value are:\n")
    print(route_value.head(10))
    topTenTotalValue = route_value["total_value"].head(10).sum()
    print(f"Overall total value: {totalValue}")
    print(f"Value of top 10 routes by trips: {topTenTotalValue}")
    valuePercentage = topTenTotalValue * 100 / totalValue
    print(f"Percentage: {valuePercentage}%")
    print("For more information check the generated topRoutesByValue.csv file")
    data = [valuePercentage, 100 - valuePercentage]#data for pie chart
    labels = ["top 10 routes\nper value", "remaining value"]#labels for pie chart
    sns.barplot(data = route_value.reset_index().head(10), x = "total_value", y = "route")#displays top 10 routes by value
    plt.show()
    plt.pie(data, labels = labels, colors = colorsPie, autopct='%.0f%%')#displays pie chart comparing the value of the top routes compared to total value
    plt.show()

def topTransport():# Function to obtain the top transport modes by value
    transports.sort_values(by=["total_value"], inplace=True, ascending=False)#sort the dataframe by value
    transports.to_csv("transportsByValue.csv")#save dataframe to an external file
    print("The transport modes in order of value are:\n")
    print(transports)
    topThreetransports = transports["total_value"].head(3).sum()
    print(f"Overall total value: {totalValue}")
    print(f"Value of top three transport modes: {topThreetransports}")
    print(f"Percentage: {topThreetransports*100/totalValue}%")
    print("For more information check the generated transportsByValue.csv file")
    sns.barplot(data = transports.reset_index(), x = "total_value", y = "transport_mode")#displays top 10 transport modes by value
    plt.show()
    transports.plot.pie(autopct="%.1f%%", subplots = True)#displays pie chart comparing transport modes
    plt.show()

def topCountries():# Function to obtain the top countries by value
    countriesOfValue.sort_values(by=["total_value"], inplace=True, ascending = False)#sort the dataframe by value
    countriesOfValue["cumulative_percentage"] = countriesOfValue["percentage"].cumsum()#add new column containing the cumulative percentage of the value
    countriesOfValue.to_csv("countriesByValue.csv")#save dataframe to an external file
    print("The top ten countries (origin for exports, destination for imports) by total value are:\n")
    print(countriesOfValue.head(10))
    topTenTotalValue = countriesOfValue["total_value"].head(10).sum()
    print(f"Overall total value: {totalValue}")
    print(f"Value of top 10 countries: {topTenTotalValue}")
    print("For more information check the generated countriesByValue.csv file")
    ax1 = sns.set_style(style=None, rc=None )
    sns.barplot(data = countriesOfValue.reset_index().head(10), x = "countries_of_value", y = "total_value", ax = ax1)#set a bar plot displaying total value by country
    ax2 = plt.twinx()#necessary to merge bar plot with line plot
    sns.lineplot(data = countriesOfValue.reset_index().head(10), x = "countries_of_value", y = "cumulative_percentage", ax = ax2, color = "black")#set a line plot displaying cumulative percentage
    plt.show()

#---------------------WHILE LOOP FOR INTERACTIVE MENU-------------------------#

condition = False #Set a condition for the loop
iterationNumber = 0 #second condition to avoid infinite loops

while condition == False and iterationNumber < 5:
    print("Welcome to the synergy logistics data analyisis program\n")
    print("Please enter a number from 1 to 4:\n")
    option = int(input("1) Top ten routes by number of trips.\n2) Top ten routes by total value.\n3) Top transport modes.\n4) Top countries by value.\n"))

    if option == 1:
        topRoutesByTrips() #calls function to determine top routes by number of trips
    elif option == 2:
        topRoutesByValue() #calls function to determine top routes by value
    elif option == 3:
        topTransport() #calls function to determine top transport modes by value
    elif option == 4:
        topCountries() #calls function to determine top countries by value
    else:
        print("The option you chose is not valid.")

    iterationNumber += 1 #avoids infinite loop
    if iterationNumber == 5: #program closes after 5 iterations
        print("You have reached the maximum number of operations. The program will close")

    else: #program allows user to make multiple requests
        print("\nWould you like to choose another option?")
        choice = int(input("1) Yes\n2) No\n"))

        if choice == 1:
            continue
        else: #closes program if user is done with it
            condition = True

    

    
