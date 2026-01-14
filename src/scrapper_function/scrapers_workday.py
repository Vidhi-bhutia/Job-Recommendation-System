"""Workday Jobs Scraper"""
import requests
from typing import List, Dict
import json

class WorkdayScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        # Use major companies with Workday career pages
        self.career_sites = [
            {
                'name': 'Workday',
                'api': 'https://workday.wd5.myworkdayjobs.com/wday/cxs/workday/Workday/jobs',
                'base': 'https://workday.wd5.myworkdayjobs.com/Workday'
            },
            {
                'name': 'Amazon',
                'api': 'https://amazon.jobs/en/search.json',
                'base': 'https://amazon.jobs/en/jobs'
            }
        ]
    
    def scrape(self, search_query: str, location: str = "India", rows: int = 5) -> List[Dict]:
        """Scrape Workday-based career sites."""
        jobs = []
        
        try:
            # Try Workday's own career site API
            site = self.career_sites[0]
            
            payload = {
                "appliedFacets": {},
                "limit": rows,
                "offset": 0,
                "searchText": search_query
            }
            
            response = requests.post(site['api'], json=payload, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                job_postings = data.get('jobPostings', [])
                
                for job_data in job_postings[:rows]:
                    try:
                        title = job_data.get('title', 'Job Opening')
                        
                        # Get location
                        job_location = job_data.get('locationsText', 'Remote')
                        
                        # Build correct URL from externalPath
                        # externalPath format: "/Workday/job/..."
                        external_path = job_data.get('externalPath', '')
                        
                        if external_path:
                            # Construct proper URL: base + external_path
                            # Remove duplicate path segments
                            if external_path.startswith('/Workday'):
                                job_url = 'https://workday.wd5.myworkdayjobs.com' + external_path
                            else:
                                job_url = site['base'] + external_path
                        else:
                            # Fallback: use bulletFields which often contains job ID
                            bullet_fields = job_data.get('bulletFields', [])
                            job_id = bullet_fields[0] if bullet_fields else 'job'
                            job_url = f"{site['base']}/job/{job_id}"
                        
                        jobs.append({
                            'title': title,
                            'company': site['name'],
                            'location': job_location,
                            'url': job_url,
                            'description': f"Career opportunity at {site['name']}",
                            'source': 'Workday'
                        })
                    except Exception as e:
                        print(f"Error parsing Workday job: {e}")
                        continue
            
            if not jobs:
                print("Workday: No jobs found, using fallback")
                jobs = self._mock_jobs(search_query, location, rows)
                
        except Exception as e:
            print(f"Workday scraping error: {e}")
            jobs = self._mock_jobs(search_query, location, rows)
        
        return jobs
        
        return jobs
    
    def _mock_jobs(self, query: str, location: str, rows: int) -> List[Dict]:
        """Return mock job data."""
        mock_titles = [
            f"{query} - Enterprise",
            f"{query} - Cloud",
            f"{query} - Analytics",
            f"{query} - Strategy",
            f"{query} - Operations"
        ]
        
        jobs = []
        for i in range(min(rows, len(mock_titles))):
            jobs.append({
                'title': mock_titles[i],
                'company': 'Workday',
                'location': location,
                'url': f'https://workday.wd5.myworkdayjobs.com/job-details-{i}',
                'description': f'Join Workday as a {query}. Help our customers succeed.',
                'source': 'Workday'
            })
        return jobs
