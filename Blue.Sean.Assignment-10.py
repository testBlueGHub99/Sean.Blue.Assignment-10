'''
******************************************************************************* 
File: Blue.Sean.Assignment-10.py
Name: Sean Blue
Date: 6/5/2020
Course: Python Programming ICT-4370

ADDITIONAL FUNCTIONALITY: Adding functionality to assignment 8 - Create a 
database table to write the historical stock data imported from the JSON file 
and retrive the data from the SQLite database to display in a graph.

DESCRIPTION: The program creates a historical stock data graph to visualize the 
			 stock closing values by purchase date for each unique stock symbol. 
			 The historical stock data is imported from a JSON file. The program
			 creates a table to store the imported data and retrives the data
			 to produce a graph.The program uses the matplotlib library to 
			 produce the graph and a stock class to represent a stock quote.
*******************************************************************************
'''

''' Import json library to read and intepret a json stock quote file '''
import json
''' Import matplotlib pyplot library to generate a line graph chart '''
import matplotlib.pyplot as plt
''' Import matplotlib to access the convert dates for use in the graph '''
import matplotlib
''' Import the datetime module and datetime function, for converting dates '''
from datetime import datetime


# Define stock quote class
class Stock():    
	"""The Stock class is used to represent company stock quote. The class has
	   a symbol attribute and defines a stock close value list and stock quote 
	   purcahse date list. The add stock close data method is used to assign
	   the stock closing values and pruchase dates to a unique stock quote. """
	   
	def __init__(self, stock_symbol):
		'''Initialize attributes to describe a stock'''
		self.stock_symbol = stock_symbol
		self.stock_close_value_list = []
		self.stock_purchase_date_list = []
		
	def add_stock_close_data(self, close_value, purchase_date):
		"""Add a stock quote closing value and purcahse date to the stock class 
		   close value list and purcahse date list attributes"""
		self.stock_close_value_list.append(close_value)
		self.stock_purchase_date_list.append(purchase_date)		
		
# Open the external JSON file to get the historical stock quote information 
with open('AllStocks.json') as stock_file_data:
	stock_data = json.load(stock_file_data)
		
		
# New Additional Functionality ################################################

''' Import database module for connecting, creating, writing, and reading from
	a sqlite database - NEW'''
import sqlite3

''' Create Database Table - NEW'''

# Define database path name
database_path = "Stocks_Historical_Data.sqlite"

# Establish a named connection to access the database
connection = sqlite3.connect(database_path)


# Create database layout for stock historical data table.
sql_create_historical_stock_table = ''' CREATE TABLE IF NOT EXISTS 
                            historical_stock_data (
                            purchase_ID     text    NOT NULL,
                            stock_symbol    text    NOT NULL,
                            purchase_date   text    NOT NULL,
                            open_price		float	NOT NULL,
                            high_price	    float   NOT NULL,
                            low_price	    float   NOT NULL,
                            close_price	    float   NOT NULL,
                            volume			float	NOT	NULL
                            ); '''
                            
# Open database connection and execute sql statements to create the 
# historical stock table. After executing the SQL statement commit the actions 
# and close the database connection
connection = sqlite3.connect(database_path)
cursor	=	connection.cursor()
cursor.execute(sql_create_historical_stock_table)
connection.commit()	
connection.close()


''' Write Data To Database - NEW'''

# Reconnect to the SQLite database
connection = sqlite3.connect(database_path)

# Establish a named cursor to enable database commands
cursor = connection.cursor()

# Define index number and set initial value to populate the stock purchase ID.
index_number = 1000

# Build the SQLite command to insert a row-record to pass to the database
for stock in stock_data:
    # Execute the sql INSERT command to place the historical stock values into 
    # the created rows of the database.
    cursor.execute("INSERT INTO historical_stock_data VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
					(index_number, \
					 stock['Symbol'], \
					 stock['Date'], \
					 stock['Open'], \
					 stock['High'], \
					 stock['Low'], \
					 stock['Close'], \
					 stock['Volume']) )
    # Increment the index number by 10 to make each purchase ID unique         
    index_number += 10

# Commit SQLite command and close the database connection
connection.commit()
connection.close()

''' Retrieve Data From Database - NEW'''

# Define a stock quote dictionary to store the information retrieved from the 
# database
stock_dictionary = {}

# Open database connection
db_connection = sqlite3.connect("Stocks_Historical_Data.sqlite")
cursor = db_connection.cursor()

# Loop through each row of the historical stock data table and retrieve the 
# purchase ID, symbol, closing value, and purchase date values. Use the values 
# to input into an instance of the Stock class and store in the stock dictionary.
for historical_stock_records in cursor.execute("SELECT purchase_ID, \
								  stock_symbol, \
								  close_price, \
								  purchase_date \
								  FROM historical_stock_data;"):
		
	# Check to see if stock symbol exist in the stock dictionary. If not then
	# add the new stock symbol to the stock dictionary.
	if historical_stock_records[1] not in stock_dictionary:
		stock_dictionary[historical_stock_records[1]] = \
								{'stock': Stock(historical_stock_records[1])}
		
	# Append the stock purchase date and closing value to the stock symbol it 
	# is associated with. Use the datetime module imported to format the date.	
	stock_dictionary[historical_stock_records[1]]['stock']. \
					add_stock_close_data(historical_stock_records[2], 
					datetime.strptime(historical_stock_records[3], '%d-%b-%y'))
                        
# End of New Functionality ####################################################	
		
		
''' Set up and Display Graph '''

# Define graph plot figure dpi and size layout
fig = plt.figure(dpi=128, figsize=(10, 6))

# Loop through stock dictionary and plot the stock closing values by purchase 
# date for each unique symbol.
for stock in stock_dictionary:
	plt.plot_date(stock_dictionary[stock]['stock'].stock_purchase_date_list, 
				  stock_dictionary[stock]['stock'].stock_close_value_list, 
				  linestyle='solid', 
				  marker='None', 
				  label=stock_dictionary[stock]['stock'].stock_symbol)
	
# Format graph by setting the title, x and y axis labels and font size. Call 
# the auto format date method to draw the date labels diagonally.
title = "Historical Stock Data"
plt.title(title, fontsize=20)
plt.xlabel('Stock Valuation Dates', fontsize=16)
fig.autofmt_xdate()
plt.ylabel("Stock Closing Prices ($)", fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=12)

# Show the line graph and legend
plt.legend()
plt.show()

