A script for the Polish e-commerce portal www.allegro.pl
The site share API under address: https://developer.allegro.pl/en/about/ (documentation in English)
The program's operation algorithm:
- script have to read input file with batch data in xls, csv, or xml format (example batch file excel in
the attachment)
- the input file will contain columns: Number, EAN, Product, Price
- each column will have entities
- a script should perform product data search on the portal www.allegro.pl,
- for each product from a batch file the program will have to search for it on www.allegro.pl
- for each product from batch file the script have to check for all listings of that product and for each
listing the script will have to pull out data (data given in the attached sample final file)
- obtained data will have to be assembled in the excel file (attached final file)
- the script should have to be able to run on my own computer
In the attachment the sample batch file and the sample final file.
Batch file:
1. it contains four columns: Number, EAN, Product, Price
2. in the first case we want the script to search for listings from phrases from column C -
Product
3. in the second case we want the script to search for listings from phrases from column B - EAN
Final file:
Just for the purpose of explanation I marked cells with colors:
1. Cells marked in red are the cells from the batch file.
2. Cells marked in green are just repeat of the main product fields (must be repeated).
3. Cells marked in blue are just blank, have no value
4. Cells marked in orange are cells to be created by script.
5. Some cells have comment, in these comment I’ve try to point you the response parameter
the column refers to, just for better understanding
All parameters in comments were from “Sample response” section from the page:
https://developer.allegro.pl/en/news/2018-07-03-listing_ofert/
Script:
1. Script should have option to choose whether we want to search based on phrases from the
column C (Product) from the batch file or based on phrases from the column B (EAN) from
the batch file.
We want to search based on phrases from the column C (Product) by default.
2. Script should have option to choose whether we want to search only in the title of offers
searchMode=REGULAR
or in titles and offers descriptions searchMode=DESCRIPTION
We want searchMode to be REGULAR by default.
3. When searching with searchMode=REGULAR script should read only first fifty (50) characters
with spaces from batch file (because titles on allegro are restricted to only fifty characters
with spaces).
4. When searching with searchMode= DESCRIPTION there is no limit with characters.
5. Script should have option to choose whether we want "fallback" parameter to be true or
false.
We want fallback to be false by default.
6. If that’s possible offers should be sorted within each product by popularity descending: from
highest to lowest ; sort –popularity.
7. Cells of Main image URL column should contain URL’s of the first photo
