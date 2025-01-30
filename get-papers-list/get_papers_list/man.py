MANUAL_TEXT = """
Usage: pubmed_search [OPTIONS] QUERY

Searches the PubMed API for a given query, filters the results, and writes them to a CSV file.

Arguments:
  QUERY                 The search query to use with the PubMed API.  This is a required argument.

Options:
  -h, --help            Show this help message and exit.
  -f, --filepath FILE   The path to the CSV file where results will be written.
                        (default: pubmed_results.csv)
  -d, --debug           Enable debugging output.
  --api-key TEXT        Your NCBI API key.  Required for some PubMed functionality.
                        If not provided, the script will attempt to use a cached key
                        or prompt for one.  Storing it in an environment variable
                        `NCBI_API_KEY` is also supported.
  --email TEXT          Your email address for PubMed API requests. Required if you provide an API key.
                        Can also be provided via the environment variable `NCBI_EMAIL`.
  --reldate INT         Filter results published with in i days.
  --date-from TEXT      Filter results published after this date (YYYY/MM or YYYY  format).
  --date-to TEXT        Filter results published before this date (YYYY/MM or YYYY format).
  --relevance           Order results by relevance (default).
  --date                Order results by date.

Example Usage:
  pubmed_search "cancer research" -f my_results.csv -r 500 --date-from 2023/01/01 --field "title"
  pubmed_search "diabetes" -d --api-key YOUR_API_KEY --email your.email@example.com
  pubmed_search "heart disease" --relevance

Notes:
  - You can obtain an NCBI API key from: https://www.ncbi.nlm.nih.gov/account/
  - Providing an API key significantly increases the rate limits for PubMed searches.
  - If you don't provide an email address and API Key, the script may not be able to access PubMed.
"""
