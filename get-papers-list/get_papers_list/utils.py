
from typing import List, Union, Optional, TypedDict
import sys
import requests
import csv
import os
import logging

## exit code imports
from get_papers_list.codes import ExitCodes

## typing defined
Row = List[ Union[ str, None]]
Table = List[ Row]

class Author(TypedDict):
    name: str
    aff: Optional[str]

class Paper(TypedDict):
    pubmedID:str
    DOP:str
    title:str
    authors:List[Author]

Papers = List[ Paper]

## setup logging
logger:logging.Logger = logging.getLogger(name='utils') # this take the logger from the main initialization file

## logger functions
def info(msg:str) -> None:
    logger.info(msg)

def debug(msg:str) -> None:
    logger.debug(msg)

def error(msg:str) -> None:
    logger.error(msg)

def critical(msg:str, code:int=1) -> None:
    logger.critical(msg)
    sys.exit(code)

## this class contains all the api request functions
class APIs:    ## any sorry for naming, i am terable in it

    BASE_URL:str = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils' ## this is base url for entrez application to access nlm database

    def __init__(
        self,
        api_key:str='',    ## achually, anyone can use the API without key on default rate
        email:str='',      ## you can use registered email address for request
    ) -> None:             ## but for increased rate you need key for API
        self.api_key:str = api_key
        self.email:str = email

    def esearch(
        self,
        terms:list[str],
        sort:str,
        reldate:int,
        mindate:str,
        maxdate:str,
    ) -> Optional[list[str]]:
        """
        this function is for search the database and store all the result in the history server of the National Library of Medicine
        ---
        OUTPUT:
            - WebEnv : It is key for getting in the history server where all the result are stored
            - query_key : It is the key for getting the result for a given terms search
        ---
        INPUT:
            - terms : It is the keys we wanted to search( you can use all search parameters )
            - sort :options [ pub_date, Author, JournalName, relevance (default) ] : It is the keys for sort the search and you can choose any given value.
            - reldate : For getting only i days old papers in Esearch
            - mindate : For getting only papers publish after a date. Format are: YYYY or YYYY/MM
            - maxdate : For getting only papers publich before a date. Format are: YYYY or YYYY/MM
        """

        url:str = self.BASE_URL + '/esearch.fcgi' # url for the Esearch utility provided

        term:str = '+'.join(terms)

        ## this is add to include only those paper have atleast one non academic author as the requirement
        ## It also light out the response and make it more easy to use and make it more lightweight and fast
        term += ' AND (Inc[affil] OR Ltd[affil] OR Corporation[affil] OR "Private Practice"[affil])'
        ## these are the parameters we are going to use
        params:dict[str, Union[ str,list[str]]] = {
            'db': 'pubmed',
            'term': term,
            'sort': sort,
            'usehistory': 'true',
            'retmax': '1',         ## this function return a papers but we take only one paper from this request to make it lightweight
            'retmode': 'json'
        }

        # we can use this service without any api key or email
        if self.api_key != '' : params['api_key'] = self.api_key
        if self.email != '' : params['email'] = self.email
        """but without api key or email we retricted to 3 requests per second and we can increase the request rate by mailing to NLM and get api key"""

        ## here we add these things into a params if they have a non default values
        if reldate != -1 : params['reldate'] = str(reldate)
        if mindate != '' : params['mindate'] = mindate
        if maxdate != '' : params['maxdate'] = maxdate

        try:
            info('Initicate the Search Request')
            ## now i don't use retry block but we can add this using a decorator and make it as function or a while loop
            response:requests.Response = requests.get(url,params=params)

            if response.status_code == 200:
                info('Request is Successful')
                result:dict[str,dict] = response.json() ## this response in json
                count:int = result.get('esearchresult',{}).get('count',0) ## total number of paper in the result
                ## printing the count of papers and if count is zero exit the code
                info(f'Total Paper Founds: {count}') if count != 0 else critical('No Paper is Found',code=ExitCodes.NO_RESULT)

                ## extracting the WebEnv and query_key for response for downloading the papers
                webEnv:str = result['esearchresult']['webenv']     # by doing this if they are not found we get the error
                query_key:str = result['esearchresult']['querykey']
                return [ webEnv, query_key ]
            else:
                error('Response is Bad')
                debug(f'Response code is : {response.status_code}')
                debug(f'Response is: {response.text}')
                critical('Bad Response', code=ExitCodes.BAD_RESPONSE)
        ## getting any request exception
        except requests.exceptions.RequestException as error_:
            info('Unable to send requests')
            debug(f'{error_}')
            critical('Somethings goes wrong', code=ExitCodes.FAIL_REQUEST)
        except Exception as error_:
            debug(f'{error_}')
        critical('Somethings goes wrong', code=ExitCodes.GENERAL_ERROR)


    def efetch(
        self,
        webEnv:str,
        query_key:str,
    ) -> Optional[str]:
        """
        this function is use for download all the papers from the history server of the nlm
        ---
        OUTPUT:
            - It return a string that contain all the data
        ---
        INPUT:
            - WebEnv : It is key for getting in the history server where all the result are stored
            - query_key : It is the key for getting the result for a given terms search
        """
        url:str = self.BASE_URL + '/efetch.fcgi'

        params:dict[ str, str] = {
            'db': 'pubmed',
            'WebEnv': webEnv,
            'query_key': query_key,
            'retmode': 'text',
            'rettype': 'medline',
        }

        # we can use this service without any api key or email
        if self.api_key != '' : params['api_key'] = self.api_key
        if self.email != '' : params['email'] = self.email

        try:
            info('Initicate the Download Request')
            ## not using retry block there
            response: requests.Response = requests.get(url,params=params)

            if response.status_code == 200:
                info('Request is Successful')
                return response.text  ## this request return a response in medline formamt that is just strings

            else:
                error('Request is Unsuccessful')
                debug(f'Response Code is: {response.status_code}')
                debug(f'Response is : {response.text}')
                critical('Bad Response', code=ExitCodes.BAD_RESPONSE)

        except requests.exceptions.RequestException as error_:
            error('Unable to Send request')
            debug(f'{error_}')
            critical('Somethings goes wrongs', code=ExitCodes.FAIL_REQUEST)
        except Exception as error_:
            debug(f'{error_}')
        critical('Something goes wrong', code=ExitCodes.GENERAL_ERROR)


    def runner(
        self,
        terms:list[str],
        sort:str,
        reldate:int,
        mindate:str,
        maxdate:str,
    ) -> Optional[str]:
        """
        this function search the pubmed using api request and return the string contain all the papers in medline format
        ---
        INPUT:
            - terms : It is the keys we wanted to search( you can use all search parameters )
            - sort :options [ pub_date, Author, JournalName, relevance (default) ] : It is the keys for sort the search and you can choose any given value.
            - reldate : For getting only i days old papers in Esearch
            - mindate : For getting only papers publish after a date. Format are: YYYY or YYYY/MM
            - maxdate : For getting only papers publich before a date. Format are: YYYY or YYYY/MM
        """
        webEnv, query_key = self.esearch(
            terms,
            sort,
            reldate,
            mindate,
            maxdate,
        ) or [ '', '']  ## this for remove the error from pyright
        return self.efetch(webEnv,query_key)


## this class contain the function that process the response data and store the useful data into
## csv file and it not take care of email because in reponse there is not emial
class Processor:

    def __init__(self) -> None:
        pass

    def rectifier(
        self,
        medline_data:str,
    ) -> list[str]:
        """
        this function convert the medline multiline data into a single line medline data array
        """
        rectified_data:list[str] = []
        for line in medline_data.splitlines():
            if line.startswith('      '):       ## because the continume line is start with six spaces
                rectified_data[-1] += line[4:]
            else:
                rectified_data.append(line)
        return rectified_data

    def convertor_and_filter(
        self,
        _Data:list[str]
    ) -> None:
        """
        this function that convert single line medline into dict
        """
        self.papers:Papers = []  ## i know thats two much
        paper:Paper = {
            "pubmedID": "",
            "DOP": "",
            "title": "",
            "authors": []
        }
        for line in _Data:
            if ( line == '' or line == ' ' ) and paper != {
                "pubmedID": "",
                "DOP": "",
                "title": "",
                "authors": []
            }:
                self.papers.append(paper)
                paper:Paper = {
                    "pubmedID": "",
                    "DOP": "",
                    "title": "",
                    "authors": []
                }
            else:
                if line.startswith('PMID- '):
                    paper['pubmedID'] = line.split('PMID- ',1)[1].strip()
                elif line.startswith('DP  - '):
                    paper['DOP'] = line.split('DP  - ',1)[1].strip()
                elif line.startswith('TI  - '):
                    paper['title'] = line.split('TI  - ')[1].strip()
                elif line.startswith('FAU - '):
                    author = line.split('FAU - ',1)[1].strip()
                    if 'authors' not in paper:
                        paper['authors'] = []
                    paper['authors'].append({
                        'name': author,
                        'aff': '',
                    })
                elif line.startswith('AD  - ') and len(paper['authors']) != 0 and paper['authors'][-1]['aff'] == '':
                    aff = line.split('AD  - ',1)[1].strip()
                    if 'University' in aff or 'Hospital' in aff:
                        paper['authors'].pop(-1)
                    else:
                        paper['authors'][-1]['aff'] = aff
        if paper:
            self.papers.append(paper)

    def preprocess(self) -> None:
        """
        this function preprocess the
        """
        self.preprocessed:Table = [ [ 'PubMedID' , 'DOP' , 'Title' , 'Author' , 'Affiliation' ] ]
        for paper in self.papers:
            if len( paper['authors'] ) == 0 :
                self.preprocessed.append( [ paper['pubmedID'] , paper['DOP'] , paper['title'] , None , None ] )
            else:
                self.preprocessed.append( [ paper['pubmedID'] , paper['DOP'] , paper['title'] , paper['authors'][0]['name'] , paper['authors'][0]['aff'] ] )
                for author in paper['authors'][1:] :
                    self.preprocessed.append( [  None , None , None , author['name'] , author['aff'] ])

    def writer(
        self,
        filepath:str
    ) -> None:
        """
        this function, write all the rectified and filtered papers into the file
        ---
        INPUT:
            - filepath: it is file path in which all the papers i write
        """
        if filepath == 'output.csv':
            filename:str = 'output.csv'
            BASE_PATH:str = os.getcwd()
            count:int = 1
            while( os.path.isfile(os.path.join( BASE_PATH , filename) )):
                filename = f'output({count}).csv'
                count += 1
            filepath = os.path.join( BASE_PATH , filename )
            info(f'All the papers is written in this file: {filepath}')

        try:
            with open(filepath,'w',newline='') as file:
                _writter = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL) ## here we adding the quoting because data contains commas
                for line in self.preprocessed:                                    ## and that make difficult to open the csv properly
                    _writter.writerow(line)
            info('Enverything is written to file')
        except Exception as error_:
            debug(f'{error_}')
            critical(f'Unable to Write to File: {filepath}', code=ExitCodes.WRITING_ERROR)

    def runner(
        self,
        medlineData:str,
        filepath:str,
    ) -> None:
        """
        this function is run all the functions
        """
        try:
            DATA:list[str] = self.rectifier(medlineData)
            self.convertor_and_filter(DATA)
            self.preprocess()
            self.writer(filepath)
        except Exception as error_:
            debug(f'{error_}')
            critical('Somethings go wrong', code=ExitCodes.GENERAL_ERROR)


### the search function this function run the upper two classes to get the desired result
def search(
    query:str,
    filepath='output.csv',
    api_key:str='',
    email:str='',
    sort:str='relevance',
    reldate:int=-1,
    mindate:str='',
    maxdate:str='',
) -> None:
    """
    this function is for run the APIs and Processor Class, it take the input then run the program and it return None
    ---
    INPUT:
        - terms : It is the keys we wanted to search( you can use all search parameters )
        - filepath : It is the path of file where all the results are write
        - api_key : It is API key to access nlm database ( any one can access it without api but with limited api calls per second )
        - email : It is a registered email that can use as the api key for high call rates
        - sort :options [ pub_date, Author, JournalName, relevance (default) ] : It is the keys for sort the search and you can choose any given value.
        - reldate : For getting only i days old papers in Esearch
        - mindate : For getting only papers publish after a date. Format are: YYYY or YYYY/MM
        - maxdate : For getting only papers publich before a date. Format are: YYYY or YYYY/MM
    """
    terms:list[ str] = query.split()

    DATA:str = APIs(api_key=api_key,email=email).runner(
        terms=terms,
        sort=sort,
        reldate=reldate,
        mindate=mindate,
        maxdate=maxdate,
    ) or ""

    if DATA.__len__() == 0 : critical('Somethings goes Wrong', code=ExitCodes.GENERAL_ERROR)

    Processor().runner(
        medlineData=DATA,
        filepath=filepath
    )
