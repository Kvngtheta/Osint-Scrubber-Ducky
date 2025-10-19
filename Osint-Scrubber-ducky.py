import requests
import argparse
import json

# Function to get LinkedIn employees via SerpAPI
def get_linkedin_employees(company_name, serpapi_key):
    # URL for SerpAPI LinkedIn People Search
    search_url = "https://serpapi.com/search.json"
    params = {
        "engine": "linkedin",           # LinkedIn engine
        "q": f"{company_name} employees",  # Search query
        "api_key": serpapi_key          # Your SerpAPI key
    }
    response = requests.get(search_url, params=params)
    data = response.json()

    # Collect names from result
    employees = []
    if 'linkedin_profiles' in data:
        for profile in data['linkedin_profiles']:
            if 'name' in profile:
                employees.append(profile['name'])
    return employees

# Function to check name/email against DeHashed API
def query_dehashed(name, dehashed_email, dehashed_key):
    url = f"https://api.dehashed.com/search?query={name}"
    response = requests.get(url, auth=(dehashed_email, dehashed_key))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed query for {name}, Status Code: {response.status_code}"}

# Main function to parse arguments and run the program
def main():
    parser = argparse.ArgumentParser(description="Scrape LinkedIn and check DeHashed for employees.")
    parser.add_argument('--company', required=True, help='Company name to search on LinkedIn')
    parser.add_argument('--serpapi', required=True, help='SerpAPI key for LinkedIn scraping')
    parser.add_argument('--dehashed_email', required=True, help='DeHashed account email')
    parser.add_argument('--dehashed_key', required=True, help='DeHashed API key')
    parser.add_argument('--output', required=True, help='Output file to store results')

    args = parser.parse_args()

    # Step 1: Scrape employees
    print(f"[+] Scraping LinkedIn for employees at {args.company}...")
    employees = get_linkedin_employees(args.company, args.serpapi)

    print(f"[+] Found {len(employees)} employee names.")

    # Step 2: Query DeHashed
    results = {}
    for name in employees:
        print(f"[*] Querying DeHashed for {name}...")
        results[name] = query_dehashed(name, args.dehashed_email, args.dehashed_key)

    # Step 3: Save to file
    with open(args.output, "w") as f:
        json.dump(results, f, indent=4)

    print(f"[+] Results saved to {args.output}")

if __name__ == "__main__":
    main()
