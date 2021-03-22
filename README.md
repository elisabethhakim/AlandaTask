# Alanda Task

Script and results to demonstrate my skills to write scrapers to collect large amount of data from websites.

## Description
In this project I have scraped information on property listings from [Purple Bricks'](https://www.purplebricks.co.uk/search/property-for-sale/?betasearch=true&page=1&searchRadius=30&searchType=ForSale&soldOrLet=false&sortBy=2&location=London) website based on real estates for sale in the greater London area. The features of interest describe the property for sale (number of bedrooms, property type and listing value in GBP). The scripts also allows the user to scrape listings in other locations and choose size of radius, but cannot choose to scrape additional parameters without developing the project further.

## Getting started

### Dependencies
The project has been developed in Python 3.9.2 and is using the following external libraries:
* requests\~=2.25.1
* bs4\~=0.0.1
* beautifulsoup4\~=4.9.3
* html5lib\~=1.1

### Installing
The project can be downloaded from [GitHub](https://github.com/elisabethhakim/AlandaTask.git).

### Executing program
#### Multi-page results
Given the amounts of properties for sale, the result of the search is likely shown on multiple pages on the website. Therefore, I have taken the approach of reading multiple URLs based on the below steps:
1. Calculate the total number of pages to loop through
	>The total number of pages are shown in the top pane of the result area and is obtained from a \<strong\> tag of the HTML code.  
        **\<strong\>number of pages\</strong\>**  
	>In order to generate the number of loops required, a URL is created using the *build_url* function, with an arbitrary page number and pre-determined radius and location. Next, a response is retieved by connecting to the server and sending a GET request using *get_res*, with an URL string as argument.  
	>Thereafter, the total number of pages is obtained by fetching the response to the *get_loop_num* function. It uses *BeautifulSoup* and the *html5lib* to parse the content of the request and is locating the \<strong\> tag which is nested within a \<span\>. Given that 10 results are stored on each page, *loop_num* is obtained by dividing the total number of properties for sale in the area by 10.

2. Retrieve property features
	>As a first step, the *get_res_tags* function is called using the retieved *loop_num* from the previous step, as well as the pre-detemined radius and location of choice as arguments.
	>For each of the pages which exist for the property search, the function generates a new URL string using *build_url* and a retrieves a response from the server using *get_res*, for which the response content is parsed with *BeautifulSoup*. All the 10 results which are showed on the page are nested within an \<ul\> tag (example below), which can be found by its *data-testid* "results-list". Once all of the pages have been looped through as described above, the *get_res_tags* returns a list of the results tags.  
        **\<ul data-testid="results-list" class="search-resultsstyled__StyledSearchResults-krg5hu-2 iaLdgK"\>...\</ul\>**  
	>In the second step of retrieving property features, the relevant features within the tags are isolated and saved in a dictionary calling the *parse_data* function. A nested loop is used to go through all the tags in the list and up to 10 properties within each tag.
	>The features of interest can be found in \<a\> tags of the html code. Each property is stored in the dictionary under a property ID, defined as the number combination found in the end of the *href* attribute. The features are obtained by getting the *aria-label* attribute and splitting the obtained string into (example below): number of bedrooms (5 bedroom), property type (detached house) and price (4250000).  
        **\<a class="property-cardstyled__StyledLink-sc-15g6092-1 eQIvCR " aria-label="5 bedroom detached house - £4,250,000" href="/property-for-sale/5-bedroom-detached-house-chigwell-1086709"\>\</a\>**  

3. Save results in a json file
	>The dictionary obtained in the previous step is structured in line with json and can be saved down using the function *store_data*. The json file will be saved down in *AlandaTask\Data\\{location\}_\{radius\}\yyyy-mm-dd* with a file name based on the the time of execution.

## Author
Elisabeth Hakim
hakim.elisabeth@gmail.com
