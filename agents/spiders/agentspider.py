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



