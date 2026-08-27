import sys
import requests

base_url = "https://api.github.com/repos"



def repository(repository) :
    url = f"{base_url}/{repository}"
    try:
        response = requests.get(url , timeout=20)
        
        
    except requests.exceptions.RequestException as error:
            print(f"Error occurred while checking the repository: {error}")
            return None
    status_code = response.status_code
    

    if response.status_code >= 200 and response.status_code < 300:
        data = response.json()

        print(f"Successs:")
        print(f"  Repository: {data.get('name', 'Unknown')}")
        print(f"  Stars: {data.get('stargazers_count', 'Unknown')}")
        return True

    elif response.status_code == 404:
        print(f"Repository not found: {repository}")
        print(f"HTTP {status_code}")
        print("This repository does not exist or has been deleted.")
        print()
        return False

    elif response.status_code == 403:
        remaining_request = response.headers.get("X-RateLimit-Remaining")
        limit = response.headers.get("X-RateLimit-Limit")

        if remaining_request == "0":
            print(f"Rate limit exceeded for repository: {repository}")
            print(f"HTTP {status_code}")
            print(f"Limit: {limit}")
            print("you have used your maximum rate limit.")
            print()
            return False
        else: 
            print(f"response code: {status_code}")
            print(f"forbidden access to: {repository}")
            print()
            return False

    elif response.status_code == 401:
        print(f"Unauthorized access for repository: {repository}")
        print(f"HTTP {status_code}")
        return False

    elif 400 <= response.status_code < 500 :
        print(f"bad request for repository: {repository}")
        print(f"http {status_code}")
        print("Client error occurred.")
        print()
        return False

    elif 500 <= response.status_code < 600:
        print(f"Server error for repository: {repository}")
        print(f"HTTP {status_code}")
        print("GitHub server error occurred.")
        print()
        return False
    
    else:
        print(f"Unexpected HTTP status code: {status_code}")
        print()
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("please provide a repository")
        sys.exit(1)

    all_good = True

    for repo in sys.argv[1:]:
        result = repository(repo)

        if result is not True:
            all_good = False

    if all_good:
        print("All repositories have been checked successfully.")
    else:
        print("Some repositories were not checked successfully.")
