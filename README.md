TwiBot
======

A twitter analyser - summaries, classification and location mapping.

Description
===========

This project aims to analyse trending tweets on twitter and put up summaries and classify and map them on a map.
The summariser uses the extractive lexrank algorithm, the classifier uses the Naive Bayes Algorithm and mapping is done using Google Maps API.


How to Run
==========

Since the application runs on flask. Run the python file analyse.py and point browser to localhost:5000 to see results.
Note: The application has many path dependencies at many places. Work is underway to automate this.

Dependencies
==========
1. Flask
2. NLTK with Tokenizer module
3. Scikit 
