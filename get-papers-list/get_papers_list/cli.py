import argparse
import logging
from typing import Any
import sys



## utils imports
from get_papers_list.utils import search

## manual import
from get_papers_list.man import MANUAL_TEXT

## logger configurations
logging.basicConfig( level=logging.INFO, format='%(asctime)s [ %(levelname)s ] - %(message)s')


## command_line interface
def main() -> None:
    """
    this is the main function that use for cli operations
    """

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Searches the PubMed API for a given query, filters the results, and writes them to a CSV file.",
            epilog="""
    Example Usage:
      pubmed_search "cancer research" -f my_results.csv -r 500 --date-from 2023/01/01 --field "title"
      pubmed_search "diabetes" -d --api-key YOUR_API_KEY --email your.email@example.com
      pubmed_search "heart disease" --relevance

    Notes:
      - You can obtain an NCBI API key from: https://www.ncbi.nlm.nih.gov/account/
      - Providing an API key significantly increases the rate limits for PubMed searches.
      - If you don't provide an email address and API Key, the script may not be able to access PubMed.
            """,
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False,
        )

    # Required argument (query)
    parser.add_argument("query", type=str, help="The search query to use with the PubMed API.")

    # Optional arguments
    parser.add_argument("-h","--help", action='store_true')
    parser.add_argument("-f", "--filepath", type=str, default="output.csv", help="The path to the CSV file (default: pubmed_results.csv)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debugging output.")
    parser.add_argument("--api-key", type=str, help="Your NCBI API key.  Required for some PubMed functionality.")
    parser.add_argument("--email", type=str, help="Your email address for PubMed API requests. Required if you provide API key.")
    parser.add_argument("--reldate", type=int, help="For getting i days olders paper for the search")
    parser.add_argument("--date-from", type=str, help="Filter results published after this date (YYYY/MM/DD format).")
    parser.add_argument("--date-to", type=str, help="Filter results published before this date (YYYY/MM/DD format).")

    # Mutually exclusive group for ordering
    group: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group()
    group.add_argument("--relevance", action="store_true", help="Order results by relevance (default).")
    group.add_argument("--date", action="store_true", help="Order results by date.")

    args:argparse.Namespace = parser.parse_args()

    ## changing the logging level
    if args.debug : logging.getLogger().setLevel( logging.DEBUG )


    ## adding manual
    if args.help:
        print(MANUAL_TEXT)
        sys.exit(0)

    arguments: dict[ str, Any] = {}  ## these are the argument we going to pass

    arguments['query'] = args.query
    arguments['filepath'] = args.filepath

    ## adding other args
    if args.api_key : arguments['api_key'] = args.api_key
    if args.email : arguments['email'] = args.email
    if args.relevance : arguments['sort'] = 'relevance'
    if args.date : arguments['sort'] = 'pub_date'
    if args.reldate : arguments['reldate'] = args.reldate
    if args.date_from : arguments['mindate'] = args.date_from
    if args.date_to : arguments['maxdate'] = args.date_to

    search(**arguments)

    sys.exit(0)


if __name__ == "__main__":
    main()
