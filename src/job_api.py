"""Job API - Web Scraping Modules"""
from .scrapper_function.scrapers_linkedin import LinkedInScraper
from .scrapper_function.scrapers_workday import WorkdayScraper

# Initialize scrapers
linkedin_scraper = LinkedInScraper()
workday_scraper = WorkdayScraper()


def fetch_linkedin_jobs(search_query, location="India", rows=5):
    """Fetch job listings from LinkedIn using web scraping."""
    try:
        return linkedin_scraper.scrape(search_query, location, rows)
    except Exception as e:
        print(f"LinkedIn fetch error: {e}")
        return []


def fetch_workday_jobs(search_query, location="India", rows=5):
    """Fetch job listings from Workday using web scraping."""
    try:
        return workday_scraper.scrape(search_query, location, rows)
    except Exception as e:
        print(f"Workday fetch error: {e}")
        return []

