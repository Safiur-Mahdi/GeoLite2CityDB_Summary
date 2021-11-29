Thank you for giving me opportunity to solve the MaxMind coding challenge, I really enjoyed while solving the problem!

I implemented the coding challenge using Python3 (3.8.10).<br><br>
I utilized functional programing to solve the problem and followed best current practices. However, the code can easily be extend to follow any other programming techniques such as OOP/MVC.<br><br>
I printed the output both in console and html file(open automatically).<br><br>
With the most viewed page, I also printed the #viewCount.<br><br>
In the assignment question, it says "Ignore all requests for images", and in the access.log file, I found there are many request starting "/images/...." such as "/images/ratings/blue-4-00.png", and if I filter with the given "/[a-f0-9]+/images/" since "+" represents "1 or more", all the request for images could not be ignored. So, I changed the regular expression pattern to  "/[a-f0-9]*/images/" where "\*" represents "0 or more" so that I can ignore all requests for images.<br><br>
Due to time constraints, I could not address any unit testing.<br><br>

How to run the code:
========================
On a standard Ubuntu system (Ubuntu 20.04 or less), at first we need to check whether python is already installed or not:<br>

Ubuntu version 20.04: python3 --version<br> 
Previous versions: python --version<br>

If python3 is not installed, please run following commands:<br>
sudo apt-get update<br>
sudo apt-get install python3<br>
Reference: https://www.makeuseof.com/install-python-ubuntu/<br>

Once, python3 is installed, we need to install "geoip2" module by following command:<br>
 
pip install geoip2<br>

Reference: https://pypi.org/project/geoip2/<br>

If pip (Pip Install Packages) is not installed, please execute following command:<br>
sudo apt install python3-pip<br>

We are now ready to run the code by following command (Ubuntu 20.04):<br>
python3 parseGeoLiteCityDB.py access.log<br>

For prior Ubuntu version:<br>
python parseGeoLiteCityDB.py access.log<br>

Files needed to run the program:
====================================
1. access.log<br>
2. GeoLite2-City.mmdb<br>

Both of the files need to be present in the same directory where parseGeoLiteCityDB.py is located. <br>
While executing the run command (python3 parseGeoLiteCityDB.py access.log), we can use different log files to get different outputs.<br>
If you want to try a different database, please change the variable name in line no. 15 in the code.<br>
I can code in such way so that we can have both (access.log file and database file) as an input, however, since the homework question says "Include a command-line program to run your code against an arbitrary file", I limited the input argument to only access.log file.<br>

Sample Outputs:
==================
User can mistakently give different inputs while running the program, I handled those situation in my code. Followings are the different case scenario:<br>
1. No input file given:<br>
python3 parseGeoLiteCityDB.py<br>
Output: <br>
