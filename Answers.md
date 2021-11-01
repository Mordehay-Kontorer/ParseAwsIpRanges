# Answers - Backend Python Developer home assignment

## Exercise 1 - make the code work:
What code changes need to be made?  
The main bug in the code is defining response = {"region":"","prefix":[]} before the loop(in line 29).  
During running over the loop (for region in regions) for combining the data of regions and prefixes  
the reponse dictionary overrides the region but not the response["prefix"].  
The list of response["prefix"] continues to expand and grows to be much larger than the expected limit(100),  
starting from the second iteration.  


The original code:
```
allResponse = []
    prefix_limit = 100
    print(regions)
    response = {"region":"","prefix":[]}          HERE is the bug
    for region in regions:
        print("****************************")
        print(f'working on region {region}')
        response["region"] = region
        i = 0
        for p in prefixs:
            if p["region"] == region and i < prefix_limit:
                response["prefix"].append({"id": i,"service":p["service"],"ip_prefix":p["ip_prefix"]})
                i += 1
        allResponse.append(response)
```

The simple solution is to define response = {"region":"","prefix":[]} line under the printings in the loop.  
This way:  
```
allResponse = []
    prefix_limit = 100
    print(regions)
    for region in regions:
        print("****************************")
        print(f'working on region {region}')
        response = {"region":"","prefix":[]} 
        response["region"] = region
        i = 0
        for p in prefixs:
            if p["region"] == region and i < prefix_limit:
                response["prefix"].append({"id": i,"service":p["service"],"ip_prefix":p["ip_prefix"]})
                i += 1
        allResponse.append(response)
```

This will keep the response["prefix"] smaller than 100.  
At line 41 the code assumes that the length of dumpResponse["prefix"] is lower than 100 and fails because some of reaponses in allResponse are filled with a higher amount of prefixes.  

What tools and steps did you use to debug the code?
The first step I took was to open the url, to see the json structure.  
A quick Google search led me to the following links:  
https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html  
https://aws.amazon.com/blogs/developer/querying-the-public-ip-address-ranges-for-aws/  

There I found extensive information on the subject(AWS IP address ranges).

Later I made prints of regions and saw that the output was received properly,  
i.e. both opening the url and receiving the regions worked properly.  
I realized pretty quickly that the problem with the code is in the append that is executed on the response ["prefix"],
so I added in the following line a print of len (response ["prefix"])ת and clearly identified the problem. 

Because the engineer left the code no so efficient, reliable or designed correctly,  
I tried to make some changes in the code. 
The changes includes the:
- **Bonus**: add logging configuration to the file, replace the print statements
- **Bonus**: provide the code to run the API

The new file  with the changes attached(was_preefix.py). 

This is the code in the file:  
``` 
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
```

## Exercise 2 - error handling:
On what areas would you add try-except to avoid unhandled exception?  

In changing the code I made, I chose to turn the program into a micro-service, with 4 functions.  
So that each of the functions has its own responsibility. This will also make it easier to check them and make sure that the transition between the steps is done correctly. 

I found it appropriate to add try-except in only one place, which seemed to me the most critical and that is the opening of the url.  
In the other steps I chose different controls / tests for end cases and in some cases I performed raise exceptions without try as needed.

What kind of framework \ module would you recommend for logging?  
Python provides a logging system as a part of its standard library, so you can quickly add logging to my application.
Python’s standard library includes a flexible built-in logging module, allowing you to create different configurations to fulfill your logging needs.
Python’s logging module consists of functions designed to allow developers to log to different destinations. They do this by defining different handlers and routing the log messages to the adequate handlers.

## Exercise 3 - expose the API:
What frameworks would you recommend? We are looking for something simple, reliable and fast
When it comes to web development on Python, there are two frameworks that are widely used: Django and Flask.
From the ground up, Flask was built with scalability and simplicity in mind. 
Flask applications are known for being lightweight, mainly when compared to their Django counterparts. 
Flask also has extensive documentation that address everything that developers need to start.
Being lightweight, easy to adopt, well-documented, and popular, Flask is a very good option for developing RESTful APIs.

## Exercise 4 - sending response to SNS:
We want to publish each region 100 prefix to SNS for further processing, no limitation on the number of messages, but should be efficient
What is the SNS message size limit?

With the exception of SMS messages, Amazon SNS messages can contain up to 256 KB of text data, including XML, JSON and unformatted text.  
Each SMS message on the other hand can contain up to 140 bytes.  
If you publish a message that exceeds the size limit, Amazon SNS sends it as multiple messages, each fitting within the size limit.  
Messages are not cut off in the middle of a word but on whole-word boundaries.  

Should we reduce the 100 limit? Is there a better way to ensure we meet the size criteria?  
Since SNS allow 140 bytes per sns message and a prefix entry is about 100 bytes, we can message every entry instead of all the 100 together.
After short readinf I found out that there are better solution:
This size limit of sns is common problem, that people have. You can only send messages that are less than 256 KiB in size, which may be not enough in some scenarios and use cases. 
Since it’s a common problem there’s a common solution — use S3 to store the payload and only send a link to the S3 object via SQS or SNS.


## Exercise 5 - running as a lambda:
Can we run this code as an AWS lambda?  
Yes.   
We can deploy every individual function as a Lambda, and create a workflow with Step Function.  
We also need to deploi ApiGateWay to invoke the above Step Function when the GET route is called. 


## Exercise 6 -  running as container:
We would need to deploy a Python 3.10 docker container, install the requiemtns.txt libraries, run the aws_prefix.py entry point, and open port 8080 then we could call the API via HTTP requests (we can add gunicorn as the Python Web Server Gateway Interface HTTP server).  
Link for more information: https://gunicorn.org/