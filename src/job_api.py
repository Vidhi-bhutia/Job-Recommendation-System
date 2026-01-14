from apify_client import ApifyClient
import os
from dotenv import load_dotenv
load_dotenv()
apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

def fetch_linkedin_jobs(search_query, location="India", rows=5):
    """Fetch job listings from LinkedIn using Apify."""
    run_input={
        "title": search_query,
        "location": location,
        "rows": rows,
        "proxy":{
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
    }
    run=apify_client.actor("hKByXkMQaC5Qt9UMN").call(run_input=run_input)
    jobs=list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs
    

def fetch_naukri_jobs(search_query, location="India", rows=5):
    """Fetch job listings from Naukri using Apify."""
    run_input={
        "keywords": search_query,
        "maxJobs": rows,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "Entry",
    }
    run=apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    jobs=list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())    
    return jobs
 
def fetch_indeed_jobs(search_query, location="India", rows=5):
    """Fetch job listings from Indeed using Apify."""
    run_input={
        "country": "India",
        "query": search_query,
        "location": location,
        "maxRows": rows,
        "level": "entry_level",
        "sort": "relevance",
        "jobType": "fulltime"
    }
    run=apify_client.actor("MXLpngmVpE8WTESQr").call(run_input=run_input)
    jobs=list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())    
    return jobs

def fetch_workday_jobs(search_query, location="India", rows=5):
    """Fetch job listings from Workday using Apify."""
    run_input={
        "startUrls": [{ "url": "https://workday.wd5.myworkdayjobs.com/wday/cxs/workday/Workday/jobs" }],
        "keyword": search_query,
        "location": location,
        "collectDetails": True,
        "postedWithin": "anytime",
        "results_wanted": rows,
        "dedupe": True,
        "cookies": None,
        "cookiesJson": None,
        "proxyConfiguration": { "useApifyProxy": True },
    }
    run=apify_client.actor("qrJ5Nq2QEhZeLvXXC").call(run_input=run_input)
    jobs=list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())    
    return jobs

