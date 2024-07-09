# Web Scraping Project Report: Scraping Real Estate Agents Data using Scrapy Framework

## Table of Contents

- [Introduction](#introduction)
- [Methodology](#methodology)
- [Data Cleaning](#data-cleaning)
- [Implementation](#implementation)
- [Challenes and Solutions](#challenges-and-solutions)
- [Result](#result)
- [Conclusion](#coclusion)
- [Referances](#referances)

## Introduction

This report documents the process of scraping real estate agents data from 'https://www.bhhsamb.com' using the Scrapy framework. The objective was to gather comprehensive agent profiles including contact details, social media links, and descriptions. The report covers methodology, implementation details, challenges encountered, and the outcomes achieved.

## Methodology

## Tools and Technologies

- **Scrapy:** Python framework for web scraping.

- **Playwright and Asyncio:** Used to handle dynamic content and enable infinite scrolling.

- **Python 3:** Programming language for scripting.

- **XPath Selectors:** Utilized for precise data extraction from HTML structures.

- **JSON:** Format chosen for data storage.

- **Ubuntu:** Operating system used for development and execution of the project.

## Target Website

The target website is 'https://www.bhhsamb.com/roster/Agents', which lists real estate agents with their profiles.

## Data Extraction Techniques

- **XPath expressions** were used to locate and extract relevant data from the HTML structure of the web pages.

- **Handling Dynamic content and Infinite scrolling** was done using Playwright to ensure all agent profiles were loaded and scraped.
  
## Data Cleaning

Data cleaning was implemented to ensure data quality and consistency:

1. **Description Cleaning:** Unwanted text such as 'About' and 'More information about me.' which is there as default in agents with no description entered was removed from descriptions using regex patterns.

2. **Handling Null Values:**

Fields that had null values was handled by Imputation.

  **job_title** - Imputed null values with 'Realtor', reflecting the predominant profession among agents.
  
  **image_url** - Replaced null values with 'No Image', considering each agent typically has a unique image.
  
  **contact_details and social_accounts** - Null values in these fields were standardized to 'N/A'.
  
  **languages** - Replaced empty values with ‘English’ assuming it is since the agents resided in a country with native language English
  
  **description** - Imputed null values with 'No description', recognizing the uniqueness of each agent's profile.

3. **Address Completeness:** Rows with incomplete addresses were filtered out to maintain data integrity.

## Implementation

Code went through three important step for the webscraping.

a. **Crawling**
Going through each of the profile urls after fetching them using Playwright since the given webpage was Javascript rendered and had infinite scrolling.

b. **Parsing**
Found all the required details about the real estate agents that needed to be collected using Xpath.

c. **Cleaning and data structuring**
All the extracted data yielded was cleaned properly and structured in the specified format.

## Challenges and Solutions

**Dynamic Content Handling:** Successfully managed infinite scrolling and dynamic loading using Playwright and Asyncio.

## Result 
 The collected data which had 1070 entries was stored in JSON format featuring fields such as name, job title, image URL, contact details, social media links, addresses, offices, languages, and description.

## Conclusion

This project successfully scraped detailed profiles of real estate agents from the target website. 

## References

Scrapy Documentation: https://docs.scrapy.org/

Playwright Documentation: https://playwright.dev/python/docs/intro


