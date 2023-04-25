# Euro Jackpot calculator
 - An application which calculates the historical acquired value of 5 numbers (Euro Numbers are not counted) on Euro Jackpot: 
 https://www.euro-jackpot.net/en/results-archive-2022
- The accumulated value is the sum of the price getting for the fix 5 for each week in a lookback period.

## Files :
- app.py
- functions.py
- /teplates
- /static

## app.py : 
This file contains the flask application implementation and by running this you will be able to run the main page (Frontend) on 
http://127.0.0.1:5000/ by launching this website, application will create an empty database and you can also enter the year , region , look-back period and a group of 5 one digit or two digit number between 0 and 50 as input parameters and by pressing submit button your inputs will be posted as a way of communicating with your backend and the backend will scrape the web site and reach the desirable results and store it in a lightweighted database by sqlite3 python library and then show the results to user by showing in the result page. 
- when the user submit a set of inputs and see the results and wants to use the webpage again for new inputs, he/she should press the result page's back button to get back to the first page, this will clear the database and prevent any conflict but if user presses the explorer's back button the result of the new inputs will be added to the previous results and the total may be wrong.

## functions.py :
This file is created as a module to be imported so that the flask application become cleaner and easier to read.

## /templates :
This is the default folder of flask module to return a template (webpage) as the result, so in an endpoint when we want to return a webpage we simply make a templates floder and put the html files there and return the render_template(webpage.html) to show that particular webpage.
- index.html is the frontend that asks for user's input
- result.index shows the results by importing from the database

## /static :
It contains the css files that are communicating with the webpages in templates folder.
- style.css which is the css for index.html
- style_result.css which is the css for result.html