from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen
from flask import Flask, jsonify
from typing import List
import logging
import json
import os

# logging configuration
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
app = Flask(__name__)

URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
PREFIX_LIMIT = 100

class ParseAwsIpRanges():
    
    """ Service parser, helps to the get, organize and present data from AWS IP address ranges(in JSON format) """
    def __init__(self):
        """ Inits ParseAwsIpRanges """
        
    def get_prefixes_list(self, url: str) -> List:
        ''' 
        Get AWS prefix list from AWS IP address ranges(in JSON format)
        
        :param url: url with addres to the .json file of the Ip's
        :return: List of all the prefixes(dictionaries)
        '''
        # urllib.request.Request object
        req = Request(url)  
        try: 
            response = urlopen(req)
        # the except HTTPError must come first, otherwise except URLError will also catch an HTTPError.
        except HTTPError as e:
            logging.error(f'The server could not fulfill the request. The Error code is: {e.code}')
            exit()
        except URLError as e:
            logging.error(f'We failed to reach a server. The reaon is: {e.reason}')
            exit()
        else:
            logging.info("get_prefixes_list completed successfully!")
            return json.loads(response.read())["prefixes"]
 
    def get_regions(self, prefixes_list: List, regions = []) -> List:
        ''' 
        Get a list of Ip prefix and return a list of all the regions of these Ip's
        
        :param prefixes_list: List og Ip prefixes(dictionaries)
        :return: List of all the the regions of these Ip's(strings)
        '''
        if prefixes_list == []:
            logging.debug("get_regions got an empty array as input")
            return []
        else:
            [regions.append(pr["region"]) for pr in prefixes_list if pr["region"] not in regions]
            logging.info("get_regions completed successfully!")
            return regions
    
    def get_responses(self, prefixes_list: List, regions: List, all_responses = []) -> List:
        '''
            Get a list of Ip prefixea and list of regions, combine the data by regions
            and return the first 100 prefix for each region

            :param prefixes_list: List og Ip prefixes(dictionaries)
            :param regions: List og Ip regions
            :return: List of dictionaries with the first 100 prefix for each region
        '''
        if prefixes_list == [] or regions == []:
            logging.debug("get_responses got an empty array as input")
            return []
        for region in regions:
            logging.info(f'working on region {region}')
            response = {"region": region,"prefix": []} 
            i = 0
            for pr in prefixes_list:
                if pr["region"] == region and len(response['prefix']) < PREFIX_LIMIT:
                    response["prefix"].append({"id": i,"service":pr["service"],"ip_prefix":pr["ip_prefix"]})
                    i += 1
            if len(response["prefix"]) <= PREFIX_LIMIT:
                logging.info(f"{region} prefixes response created successfully ")
            else:
                logging.error("Response above size limit!")
                raise Exception("Response above size limit!")
            all_responses.append(response)
        logging.info("get_responses completed successfully!")
        return all_responses

    def jsonify_responses(self, all_responses:List) -> str:
        '''
            Get a list of all_responses and jsonify them.

            :param all_responses: List of dictionaries with the first 100 prefix for each region
            :return: jsonify of the list
        '''
        logging.info("jsonify_responses completed successfully!")
        return jsonify(all_responses)
 
def get_file_size(file_path):
    size = os.path.getsize(file_path)
    return size 
        
# expose the API
@app.route("/get_prefix", methods=['GET'])
def get_prefix():
    # i.e. http://127.0.0.1:8080/get_prefix
    srv = ParseAwsIpRanges()
    prefixes_list = srv.get_prefixes_list(URL)
    regions = srv.get_regions(prefixes_list)
    all_responses = srv.get_responses(prefixes_list, regions)
    jsonify_responses = srv.jsonify_responses(all_responses)
    return jsonify_responses

if __name__ == "__main__":
    # prefix_size = get_file_size('Python-Backend/example.json') # check a size of a prefix
    # print('File size: '+ str(prefix_size) +' bytes')  # File size: 10692 bytes
    app.run(debug=True, port=8080)