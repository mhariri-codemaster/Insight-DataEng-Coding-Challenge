# Anomaly Detection Code

This code is used to detect anomalies in purchase orders submitted through a stream log. The code first reads the history of previous purchase orders made by customers and saves them into a record, as well as friend/unfriend requests submitted by those customers to form a social network. New purchase orders and friend/unfriend requests are then used to update the record and network as they are recieved. The code checks every new purchase order of a customer against previous ones in the customer's social network and decides wether it was an anomaly. When all streaming information is read, the code returns a file with a list of all anomalous purchase submissions.  

## Approach

I found that simply scrolling through the purchase records backwards and looking for the last 'T' purchases in a given customers social network is faster than storing the purchases for each customer and then collecting the ones in the social network, sorting, and picking the last 'T' records.

## Directory

The main directory contains the following files/folders:
-insight_testsuit
--tests
---test_1
----log_input
----log_output
--run_tests.sh
-log_input
--batch_log.json
--stream_log.json
-log_output
--flagged_purchases.json
-src
--Main.py
--Function_Definitions.py
-README.md
-run.sh

### File and Folder Description

* **insight_testsuit:** It contains "tests" which has the test folders used to perform the tests on the code. I only included one test folder "test_1". "run_tests.sh" can be used to automate running the tests from shell terminal. Simply go to the ./insight_suite directory and type ./run_tests.sh
* **log_input:** It has two files, "batch_log.json" which contains the information needed to build the initial records and social network, and "stream_log.json" which contains the new purchase submissions and social network updates from which anomalies will be detected.
* **log_output:** It is used to store the output file "flagged_purchases" which has all the anomalies found.
* **src:** It has the Python code files "Main.py" which is the main file that reads the input and writes the output files, and "Function_Definitions.py" which contains all the functions used by "Main.py"
* **README.md**: It is the readme file.
* **run.sh**: It is used to run the code from shell terminal for the datasets in "log_input". To run, simply type ./run.sh and make sure you have the correct version of python installed. See next section for further details.

## Prerequisites

The code is written in Python 3.5.2 but should run on Python 3.1 or higher. It will also run in Python 2.7 or higher. If Python 2.7 is preferred, make sure to modify the run.sh file so that it uses:
python2.7 ./src/Main.py
instead of
python3 ./src/Main.py

### Additional Libraries/Depndencies

I did not use any additional libraries besides those standard ones available in Python:
-numpy
-json
-os
-collections/OrderedDict
If Python 3.1 or 2.7 or higher are used, no installations are required

## Authors

* **Mohamed Hariri Nokob**
