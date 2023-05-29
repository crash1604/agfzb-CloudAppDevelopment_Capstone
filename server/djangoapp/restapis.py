import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
import time


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, apikey=False, **kwargs):
    print(kwargs)
    print("GET from {}".format(url))
    # try:    
    response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    if apikey:
        params = dict()
        params["text"] = kwargs["text"]
        params["version"] = kwargs["version"]
        params["features"] = kwargs["features"]
        params["return_analyzed_text"] = kwargs["return_analyzed_text"]
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', apikey))
    # except:
        # print("Network Error")
    # print("*********************")
    print(response)
    if response:
        status_code = response.status_code
        print("With status {}".format(status_code))
        json_data = json.loads(response.text)
        # print(json_data)
        return json_data
    else:
        print("Network Error")
        return {}

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {}".format(url))
    response = requests.post(url, headers={'Content-Type':'application/json'}, 
                             params=kwargs, json=json_payload) 
    
    status_code = response.status_code
    print("With status {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data
    

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results=[]
    # - Call get_request() with specified arguments
    json_result = get_request(url)
    print("*-*-*-*-*-*-*")
    print(json)
    if json_result:
        json_result = {"rows": json_result}
        dealers = json_result["rows"]
        # - Parse JSON results into a CarDealer object list
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj =  CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], lon=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_by_id_from_cf(url, id=None):
    results = []
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
        
    # print('json_result from line 31', json_result)
    if json_result:
        # Get the row list in JSON as dealers
        # For each dealer object
        dealers=json_result
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], lon=dealer_doc["long"], full_name=dealer_doc["full_name"],
                                
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc["short_name"])
            results.append(dealer_obj)
    return results


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Perform a GET request with the specified dealer id
    json_result = get_request(url, id=dealer_id)
    # print("*-*-*-*-*-*-*-*")
    # print(json_result)
    # print("*-*-*-*-*-*-*-*")
    if json_result:
        # Get all review data from the response
        reviews = json_result["data"]["docs"]
        # For every review in the response
        for review in reviews:
            # Create a DealerReview object from the data
            # These values must be present
            review_content = review["review"]
            id = review["_id"]
            name = review["name"]
            purchase = review["purchase"]
            dealership = review["dealership"]

            if purchase:
                # These values may be missing
                car_make = review["car_make"]
                car_model = review["car_model"]
                car_year = review["car_year"]
                purchase_date = review["purchase_date"]

                # Creating a review object
                review_obj = DealerReview(dealership=dealership, id=id, name=name, 
                                          purchase=purchase, review=review_content, car_make=car_make, 
                                          car_model=car_model, car_year=car_year, purchase_date=purchase_date
                                          )

            else:
                print("Something is missing from this review. Using default values.")
                # Creating a review object with some default values
                review_obj = DealerReview(
                    dealership=dealership, id=id, name=name, purchase=purchase, review=review_content)

            
            # Analysing the sentiment of the review object's review text and saving it to the object attribute "sentiment"
            sentiment = analyze_review_sentiments(review_obj.review)
            print(f"sentiment: {review_obj.sentiment}")
            review_obj.sentiment=sentiment

            # Saving the review object to the list of results
            results.append(review_obj)
            
        print(results)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/705eba87-1d21-41e6-9f57-a9fe916aa917" 

    api_key = "l7GoM7Ys4v9xhHq8S6IvTBAgGx1rI_QDPBd1_lmua3gK" 

    authenticator = IAMAuthenticator(api_key) 

    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 

    natural_language_understanding.set_service_url(url) 

    response = natural_language_understanding.analyze( text=text ,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 

    label=json.dumps(response, indent=2) 

    label = response['sentiment']['document']['label'] 

    return(label) 
    
