Thank you for giving me the opportunity to solve the MaxMind coding challenge, I really enjoyed while solving the problem.

1. I implemented the coding challenge using Python3 (3.8.10).
2. I utilized functional programming to solve the problem and followed the best current coding practices. However, the code can easily be extended to follow any other design techniques such as OOP/MVC.
3. I printed the output both in console and Html file (open automatically if GUI supports).
4. With the most viewed page, I also printed the #viewCount.
5. In the assignment question, it says "Ignore all requests for images", and in the access.log file, I found there are many requests starting "/images/...." such as "/images/ratings/blue-4-00.png", and if I filter with the given "/[a-f0-9]+/images/" since "+" represents "1 or more", all the request for images could not be ignored. So, I changed the regular expression pattern to  "/[a-f0-9]*/images/" where "\*" represents "0 or more" so that I can ignore all requests for images.
6. I also printed the total execution time with different access.log files. 
7. I uploaded the different log files if needed.

How to run the code:
========================
On a standard Ubuntu system (Ubuntu 20.04 or less), at first, we need to check whether Python is already installed or not:<br>

Ubuntu version 20.04:<br>
python3 --version<br><br> 
Prior Ubuntu versions:<br>
python --version<br>

If python3 is not installed, please run the following commands:<br>
sudo apt-get update<br>
sudo apt-get install python3<br>
Reference: https://www.makeuseof.com/install-python-ubuntu/<br>

Once, python3 is installed, we need to install the "geoip2" module by following command:<br>
 
pip install geoip2<br>

Reference: https://pypi.org/project/geoip2/<br>

If pip (Pip Install Packages) is not installed, please execute the following command:<br>
sudo apt install python3-pip<br>

We are now ready to run the code by the following command (Ubuntu 20.04):<br>
python3 parseGeoLiteCityDB.py access.log<br>

For prior Ubuntu version:<br>
python parseGeoLiteCityDB.py access.log<br>

Files needed to run the program:
====================================
1. access.log<br>
2. GeoLite2-City.mmdb<br>

Both of the files need to be present in the same directory where parseGeoLiteCityDB.py is located. <br><br>
While executing the run command (python3 parseGeoLiteCityDB.py access.log), we can use different log files to get different outputs.<br><br>
If you want to try a different database, please change the variable name in line no. 15 in the code.<br><br>
I can code in such a way so that we can have both (access.log file and database file) as an input, however, since the homework question says "Include a command-line program to run your code against an arbitrary file", I limited the input argument to only access.log file.<br><br>
If needed, please download the "GeoLite2-City.mmdb" from here: https://drive.google.com/drive/folders/1Squ0xtr2QCDPoGq6TyIkS-_0HjA2yMib?usp=sharing

Sample Outputs:
==================
Output 1:
=========
ubuntu@ip-172-31-45-47:~/maxmind$ python3 parseGeoLiteCityDB.py access.log<br><br>
Most Viewed Country:<br>
Country :: #Most View :: "The most viewed page" (#viewCount)<br>
============================================================<br>
United States :: 13905 :: "/region/1" (61)<br>
Netherlands :: 3216 :: "/search/by-lat-long/9.250043,-83.859123/filter/category_id=1;category_id=2;category_id=3;category_id=4;category_id=5;category_id=6;category_id=7;category_id=8;category_id=9?limit=10;unit=km;distance=10" (11)<br>
China :: 1466 :: "/entry/" (9)<br>
Germany :: 1244 :: "/entry/20252" (26)<br>
France :: 702 :: "/entry/2299" (4)<br>
Russia :: 658 :: "/region/659" (3)<br>
United Kingdom :: 304 :: "/region/52" (7)<br>
Canada :: 221 :: "/entry/6843" (3)<br>
Mexico :: 120 :: "/region/1" (2)<br>
Israel :: 66 :: "/site/recent.atom?entries_only=1" (11)<br><br>

Most Viewed US States:<br>
States :: #Most View :: "The most viewed page" (#viewCount)<br>
============================================================<br>
Washington :: 2400 :: "/region/1" (17)<br>
Virginia :: 2278 :: "/entry/4628" (8)<br>
California :: 410 :: "/location/most_recent_vendors.rss?location_id=5" (22)<br>
New York :: 174 :: "/region/1" (5)<br>
Delaware :: 171 :: "/region/1503" (2)<br>
Michigan :: 153 :: "/region/447" (2)<br>
Texas :: 152 :: "/region/218" (10)<br>
Minnesota :: 131 :: "/region/13" (21)<br>
Illinois :: 116 :: "/region/1766" (4)<br>
New Jersey :: 96 :: "/entry/near/40.7458%2C-74.0321/filter/category_id=1;veg_level=2;allow_closed=0?limit=10;order_by=distance;address=Your+location" (4)<br>

Summary:<br>
Total valid IP processed: 22454<br>

Unknown Country list: (total 3)<br>
['193.202.255.201', '66.249.93.72', '66.249.81.72']<br>

Unknown states found: 790<br>

Total execution time: 13.11 seconds.<br>

I also experimented with an altered access.log file, at first reducing the total number of lines by half, and then only having the first 500 lines. So my code handles the situation correctly: "where there are less than 10 states or countries with visitors, only show those which have at least one visitor". Corresponding outputs: <br><br>

Output 2:
=========
Using 25037 lines of access.log file:<br>
ubuntu@ip-172-31-45-47:~/maxmind$ python3 parseGeoLiteCityDB.py access_half.log<br>
Most Viewed Country:<br>
Country :: #Most View :: "The most viewed page" (#viewCount)<br>
============================================================<br>
United States :: 13905 :: "/region/1" (61)<br>
Netherlands :: 3216 :: "/search/by-lat-long/9.250043,-83.859123/filter/category_id=1;category_id=2;category_id=3;category_id=4;category_id=5;category_id=6;category_id=7;category_id=8;category_id=9?limit=10;unit=km;distance=10" (11)<br>
China :: 1466 :: "/entry/" (9)<br>
Germany :: 1244 :: "/entry/20252" (26)<br>
France :: 702 :: "/entry/2299" (4)<br>
Russia :: 658 :: "/region/659" (3)<br>
United Kingdom :: 304 :: "/region/52" (7)<br>
Canada :: 221 :: "/entry/6843" (3)<br>
Mexico :: 120 :: "/region/1" (2)<br>
Israel :: 66 :: "/site/recent.atom?entries_only=1" (11)<br>

Most Viewed US States:<br>
States :: #Most View :: "The most viewed page" (#viewCount)<br>
============================================================<br>
Washington :: 2400 :: "/region/1" (17)<br>
Virginia :: 2278 :: "/entry/4628" (8)<br>
California :: 410 :: "/location/most_recent_vendors.rss?location_id=5" (22)<br>
New York :: 174 :: "/region/1" (5)<br>
Delaware :: 171 :: "/region/1503" (2)<br>
Michigan :: 153 :: "/region/447" (2)<br>
Texas :: 152 :: "/region/218" (10)<br>
Minnesota :: 131 :: "/region/13" (21)<br>
Illinois :: 116 :: "/region/1766" (4)<br>
New Jersey :: 96 :: "/entry/near/40.7458%2C-74.0321/filter/category_id=1;veg_level=2;allow_closed=0?limit=10;order_by=distance;address=Your+location" (4)<br>

Summary:<br>
Total valid IP processed: 22454<br>

Unknown Country list: (total 3)<br>
['193.202.255.201', '66.249.93.72', '66.249.81.72']<br>

Unknown states found: 790<br>

Total execution time: 13.06 seconds.<br>

Output 3:
=========
Using only first 500 lines of access.log file:<br>
ubuntu@ip-172-31-45-47:~/maxmind$ python3 parseGeoLiteCityDB.py access_500linesOnly.log<br>
Most Viewed Country:<br>
Country :: #Most View :: "The most viewed page" (#viewCount)<br>
============================================================<br>
United States :: 162 :: "/entry/5023" (3)<br>
Netherlands :: 42 :: "/entry/near/0%2C0/filter?unit=mile;distance=25;sort_order=ASC;page=;order_by=distance;address=34034;limit=" (1)<br>
China :: 21 :: "/entry/15205" (1)<br>
Switzerland :: 6 :: "/entry/15603" (2)<br>
Germany :: 4 :: "/region/60" (1)<br>
France :: 3 :: "/entry/656" (1)<br>
Canada :: 2 :: "/entry/2708" (1)<br>
Israel :: 1 :: "/site/recent.atom?entries_only=1" (1)<br>

Most Viewed US States:<br>
States :: #Most View :: "The most viewed page" (#viewCount)<br>
============================================================<br>
Washington :: 41 :: "/entry/1817" (1)<br>
Ohio :: 5 :: "/entry/5023" (3)<br>
California :: 3 :: "/location/view.html?location_id=174&new_query=1" (1)<br>
Texas :: 3 :: "/region/2" (2)<br>
Arizona :: 2 :: "/site/help" (1)<br>
Virginia :: 1 :: "/entry/18992" (1)<br>

Summary:<br>
Total valid IP processed: 242<br>

Unknown Country list: (total 1)<br>
['193.202.255.201']<br>

Unknown states found: 33<br>

Total execution time: 0.14 seconds.<br>

User can mistakently give different inputs while running the program, I handled those situation in my code. Followings are the different case scenario:<br><br>
1. No input file given:<br>
ubuntu@ip-172-31-45-47:~/maxmind$ python3 parseGeoLiteCityDB.py<br>
Please provide ONLY the 'access.log' file as the first argument.<br><br>
2. More than 1 input file given:<br>
ubuntu@ip-172-31-45-47:~/maxmind$ python3 parseGeoLiteCityDB.py access_500linesOnly.log GeoLite2-City.mmdb<br>
Please provide ONLY the 'access.log' file as the first argument.<br><br>
3. Typo while executing the command (spelling mistake of the access.log file):<br>
ubuntu@ip-172-31-45-47:~/maxmind$ python3 parseGeoLiteCityDB.py access_500linesOnly.log GeoLite2-City.mmdbasdfasdf
Please provide ONLY the 'access.log' file as the first argument.

Dependencies
=============
I imported the following modules:<br><br>
import re<br>
import sys<br>
import time<br>
import os.path<br>
import webbrowser<br>
import geoip2.database<br><br>
Generally, all the above modules come with the installing of Python3 and geoip2<br>

Addressing Evaluation criteria:
===============================
My code supports all of the evaluation criteria. Here are some of the points I want to emphasize:<br>
1. I divided every possible subtask to a different function to understand the code easily
2. I provided necessary comments where necessary
3. The code is written in a modern style for the language: I used f-Strings, \_\_name\_\_, dictionary, etc.
4. I handled all the possible exceptions using Python "Try, except, else"

Addressing Bonus Points:
===============================
1. I wrote the API documentation clearly in the code. 
2. I did the functional tests. Due to time constraints, I could not write the unit tests.
