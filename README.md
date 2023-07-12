# zillow

This program has two driver scripts, the first one "zil_rel" scrapes the initial realtor list for a given location and writes all the realtor names and links to their profile to an Excel file. 
The second script, "find_person" goes to that profile and prints a txt file with all the company and realtors info.
"scrape_fun" contains helper functions that help both scripts.

To run the program, first run the zil_rel.py script and wait for it to finish. Then run the find_person.py script and then check out the txt file. Replace the URL in zil_rel.py with another region if you want to look at other realtors. 

Examples of the Excel and txt files are given for Moscow, ID. Note that I did not run for all possible realtors because of time and access to Zillow, so this project still has work to do regarding scaling.
