Thank you for giving me opportunity to solve the MaxMind coding challenge, I really enjoyed while solving the problem!

I implemented the coding challenge using Python3 (3.8.10)
I utilized functional programing to solve the problem and followed best current practices. However, the code can easily be extend to follow any other programming techniques such as OOP/MVC.
I printed the output both in console and html file(open automatically).
With the most viewed page, I also printed the #viewCount
Due to time constraints, I could not focus on the optimization of the code.
Due to time constraints, I could not address any unit testing.

How to run the code:
========================
On a standard Ubuntu system (Ubuntu 20.04 or less), at first we need to check whether python is already installed or not:

Ubuntu version 20.04: python3 --version 
Previous versions: python --version

If python3 is not installed, please run following commands:

sudo apt-get update
sudo apt-get install python3 

Reference: https://www.makeuseof.com/install-python-ubuntu/

Once, python3 is installed, we need to install "geoip2" module by following command:
 
pip install geoip2

Reference: https://pypi.org/project/geoip2/

If pip (Pip Install Packages) is not installed, please execute following command:
sudo apt install python3-pip

We are now ready to run the code by following command (Ubuntu 20.04):
python3 parseGeoLiteCityDB.py access.log

For prior Ubuntu version:
python3 parseGeoLiteCityDB.py access.log

Files needed to run the program:
====================================
1. access.log
2. GeoLite2-City.mmdb

Both of the files need to be present in the same directory where parseGeoLiteCityDB.py is located. 
While executing the run command (python3 parseGeoLiteCityDB.py access.log), we can use different log files to get different outputs.
If you want to try a different database, please change the variable name in line no. 15 in the code.
I can code in such way so that we can have both (access.log file and database file) as an input, however, since the homework question says "Include a command-line program to run your code against an arbitrary file", I limited the input argument to only access.log file.

Sample Outputs:
==================
User can mistakently give different inputs while running the program, I handled those situation in my code. Followings are the different case scenario:
1. No input file given:
python3 parseGeoLiteCityDB.py
Output: 
