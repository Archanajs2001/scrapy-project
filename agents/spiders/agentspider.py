#get the profile urls using playwright 

import nest_asyncio
import asyncio
from playwright.async_api import async_playwright

# Apply the nest_asyncio patch to allow nested event loops
nest_asyncio.apply()

async def fetch_links():
    base_url = 'https://www.bhhsamb.com'
    url = base_url + '/roster/Agents'
    profile_links = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  
        page = await browser.new_page()

        await page.goto(url)

        # Function to perform infinite scrolling
        async def scroll_infinite():
            previous_height = await page.evaluate("document.body.scrollHeight")
            while True:
                # Scroll to the bottom of the page
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                
                # Wait for new content to load
                await page.wait_for_timeout(3000)  # Adjust time as needed based on load speed
                
                # Get the new height of the page
                new_height = await page.evaluate("document.body.scrollHeight")
                
                if new_height == previous_height:
                    break  # Exit the loop if no more content is loaded
                
                previous_height = new_height  # Update previous height to new height for the next iteration

        # Perform infinite scrolling to load all dynamic content
        await scroll_infinite()

        # Wait for a bit more time to ensure all content is loaded
        await page.wait_for_timeout(2000)  # Additional wait time after scrolling

        # Extract all links that start with '/bio/'
        bio_links = await page.query_selector_all("a[href^='/bio/']")

        #print(f"Total number of links found: {len(bio_links)}")

        # Collect the href attribute of each link and prepend the base URL
        for link in bio_links:
            href = await link.get_attribute('href')
            if href:
                full_link = base_url + href
                profile_links.append(full_link)

        await browser.close()
    return profile_links

# Function to run the async function in a Jupyter Notebook or similar environment
def get_links():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_links())

# Fetch the profile links
profile_links = get_links()

#Print the profile links
print(profile_links)



#spider

import scrapy
import re

class AgentsSpider(scrapy.Spider):
    name = "agent"
    allowed_domains = ['bhhsamb.com']
    start_urls = ['https://www.bhhsamb.com/roster/Agents']

    def parse(self, response):
        # Use the links obtained from Playwright
        global profile_links
        for link in profile_links:
            yield response.follow(link, callback=self.parse_agents)

    def parse_agents(self, response):
        name = response.xpath('//div[@class="site-global-container"]//p[@class="rng-agent-profile-contact-name"]/text()').get().strip()
        job_title = response.xpath('//div[@class="site-global-container"]//p[@class="rng-agent-profile-contact-name"]/span/text()').get()
        image_url = response.xpath('//div[@class="site-global-container"]//article[@class="rng-agent-profile-main"]/img/@src').get()
        address1 = response.xpath('//div[@class="site-global-container"]//li[@class="rng-agent-profile-contact-address"]//strong/text()[1]').get().strip()
        address2 = response.xpath('//div[@class="site-global-container"]//li[@class="rng-agent-profile-contact-address"]//strong/following::text()').get().strip()
        languages = response.xpath('//div[@class="site-global-container"]//p[@class="rng-agent-profile-languages"]/text()').getall()
        phone = response.xpath('//div[@class="site-global-container"]//li[@class="rng-agent-profile-contact-phone"]/a/@href').get().replace('tel:', '')
        facebook = response.xpath('//div[@class="site-global-container"]//li[@class="social-facebook"]/a/@href').get()
        twitter = response.xpath('//div[@class="site-global-container"]//li[@class="social-twitter"]/a/@href').get()
        linkedin = response.xpath('//div[@class="site-global-container"]//li[@class="social-linkedin"]/a/@href').get()
        youtube = response.xpath('//div[@class="site-global-container"]//li[@class="social-youtube"]/a/@href').get()
        pinterest = response.xpath('//div[@class="site-global-container"]//li[@class="social-pinterest"]/a/@href').get()
        instagram = response.xpath('//div[@class="site-global-container"]//li[@class="social-instagram"]/a/@href').get()
        website = response.xpath('//div[@class="site-global-container"]//li[@class="rng-agent-profile-contact-website"]/a/@href').get()
        email = response.xpath('//div[@class="site-global-container"]//li[@class="rng-agent-profile-contact-email"]/a/@href').get()
        description = response.xpath('//div[@class="site-global-container"]//article[@class="rng-agent-profile-content"]//text()').getall()
        #response.xpath('//div[@class="site-global-container"]//article[@class="rng-agent-profile-content"]//p//text()').getall()    

        #cleaning the data

        # handling null values with imputation

        if not job_title:
            job_title = 'Realtor'  #since more than 95% of agents have their job title as 'Realtor' 

        if not image_url:
            image_url = 'No Image'  #since its unique to each we cant impute 

        if not languages:
            languages = ['English']  #assuming 'English' as default language since all these agents live in a country with native language as English

        na = [phone, facebook, twitter, linkedin, youtube, pinterest, instagram]

        for i in na:
            if not i:
                i = 'N/A'   #since urls are unique choosing to impute with place holder 'N/A'


        # making a dict to hold all social accounts

        social_accounts = {
            'facebook': facebook,
            'twitter': twitter,
            'linkedin': linkedin,
            'youtube': youtube,
            'pinterest': pinterest,
            'instagram': instagram
        }

        #creating format for address

        address = f"{address1}, {address2}"

        
        #creating a dict to hold all contact details

        contact_details = {
            'tel': phone,
            'email': email, 
            'website': website
        }

        
        # deleting 'About' and 'More information about me' which is there in description for even agents who havent entered description.
        #to make a distinction agents who actually have valid description and those who dont.

        def clean_description(description):
            # Regex pattern to match 'About' followed by 0 to 2 words
            about_pattern = re.compile(r'\bAbout\b(\s+\w+){0,2}')

            # Clean and concatenate the description into a single string
            cleaned_description = ' '.join([
                about_pattern.sub('', text.strip()).replace('More information about me.', '')
                for text in description if text.strip()
            ])

            return cleaned_description.strip() or 'No description'
    

        # Clean the description
        cleaned_description = clean_description(description)

                
        # creating a new variable to yield from webpage data

        offices = address2.split(',')[0] + ' Office'

    
        
        yield {
            'name': name,
            'job_title': job_title,
            'image_url': image_url,
            'address': address,
            'contact_details': contact_details,
            'social_accounts': social_accounts,
            'offices': offices,
            'languages': languages,
            'description': cleaned_description
        }
