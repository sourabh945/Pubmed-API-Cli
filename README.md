# PubMed Search CLI Tool
----
## **Project Overview**
This command-line tool searches the PubMed API for academic papers with alteast on non academic author based on user-defined queries, filters the results, and saves the data in a CSV file. The tool supports advanced search features such as sorting by publication date and relevance. It is developed using Python and Poetry for dependency management.

---

## **Features**
- Search PubMed for academic papers with non-academic author based on custom queries.
- Supports filtering by publication dates and relevance.
- Save results in CSV format.
- Search the paper using NLM Entrez Eutils ( PubMed API ) and save them into history server.
- Fetch papers using PubMed API history server.
- Handles large requests efficiently with lightweight data handling.
- Sorting and Filtering done using the NLM server and database.

---

## **Installation**

### **Prerequisites**
- Python 3.9 or higher
- Poetry (for dependency management)

### **Setup Instructions**
```bash
# Clone the repository
git clone https://github.com/sourabh945/Pubmed-API-Cli.git
# Install dependencies using Poetry
poetry install
```

---

## **Usage**

### **Basic Command**
```bash
get-papers-list "<search-query>"
```

### **Command Options**
| Option        | Description                                       |
|---------------|---------------------------------------------------|
| -h, --help    | Show the help message                             |
| -f, --filepath| Path to save the CSV results (default: output.csv) |
| -d, --debug   | Enable debugging output                            |
| --api-key     | Your NCBI API key                                  |
| --email       | Your email address for API requests               |
| --reldate     | Filter results within i days                      |
| --date-from   | Filter results after a given date                 |
| --date-to     | Filter results before a given date                |
| --relevance   | Order results by relevance (default)              |
| --date        | Order results by date                              |

### **Example Commands**
```bash
get-papers-list "cancer[title] research" -f my_results.csv --reldate 500 --date-from 2023/01/01
get-papers-list "diabetes" -d --api-key YOUR_API_KEY --email your.email@example.com
get-papers-list "heart disease" --relevance
```

---

## **Example Output**
The tool will save the search results in a CSV file with columns like `PubMedID`, `DOP`, `Title`, `Author`, and `Affiliation`.

### **Sample CSV Row:**
```
PubMedID,DOP,Title,Author,Affiliation
12345678,2023-01-01,Effect of Heart Disease Treatments,John Doe,Private Research Lab
```

---

## **Development Details**

### **Code Structure**
- `cli.py`: Main entry point for the command-line interface.
- `man.py`: Manual and usage text definitions.
- `utils.py`: Contains utility functions, API requests, and result processing.

### **API Functions**
- `APIs.esearch()`: Search PubMed for results.
- `APIs.efetch()`: Fetch data from PubMed history server.
- `Processor.writer()`: Write search results to CSV.

---

## **Exit Codes**
| Exit Code | Description        |
|-----------|--------------------|
| 1         | General error      |
| 2         | No result found    |
| 3         | Bad response       |
| 4         | Request failure    |
| 5         | Writing error      |

---

## **Testing**

To test the tool, run the following commands:
```bash
poetry run get-papers-list "cancer research" --reldate 30
```
Enable debugging with:
```bash
poetry run get-papers-list "diabetes research" -d
```

---

## **Contribution Guidelines**
Contributions are welcome!

### **Steps to Contribute:**
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a pull request.

---

## **License**
This project is licensed under the MIT License.

---

## **Contact**
For questions, please reach out to:
- **Your Name:** [ sheokand.sourabh.anil@gmail.com ](mailto:sheokand.sourabh.anil@gamil.com)
- **GitHub Repository:** [ https://github.com/sourabh945/Pubmed-API-Cli.git ]( https://github.com/sourabh945/Pubmed-API-Cli.git )

---

## **LLM Used**
I use Google Gemini 1.5 Flash and ChatGPT 4o. Here are the Link of Session:
- **Google Gemini:** [ https://g.co/gemini/share/e867f03288ae ]( https://g.co/gemini/share/e867f03288ae )
- **ChatGPT:** [ https://chatgpt.com/share/679bc9b0-0e58-8010-b356-97d59431ebde ]( https://chatgpt.com/share/679bc9b0-0e58-8010-b356-97d59431ebde )
---
## **Note**
Please give me suggest and contribute to the repo. And if you wanted please also checkout my other repos [ https://github.com/sourabh945 ]( https://github.com/sourabh945 )
