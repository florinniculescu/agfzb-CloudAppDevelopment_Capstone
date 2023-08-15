import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url,api_key, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    if (api_key != 0):
        try:
            # Call get method of requests library with URL and parameters
                print("authorization call stated ...")
                response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs,
                                         auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        except:
            # If any error occurs
            print("Network exception occurred")
    else:
        try:
            print("non-auth call initiated ...")
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        except:
            # If any error occurs
            print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print(json_payload)
    print("GET from {} ".format(url))
    try:
            print("non-auth post call initiated ...")
            response = requests.post(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = response.text
    return json_data
    
# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,0)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    dealer_id = str(dealer_id)
    # Call get_request with a URL parameter
    json_result = get_request(url,0,dealerid=dealer_id)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["docs"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(car_make=review_doc["car_make"], car_model=review_doc["car_model"],
                                   car_year=review_doc["car_year"], dealership=review_doc["dealership"],
                                   id=review_doc["id"],
                                   name=review_doc["name"], purchase=review_doc["purchase"],
                                   purchase_date=review_doc["purchase_date"],
                                   review=review_doc["review"],
                                   sentiment=review_doc["review"])
            review_obj.sentiment = analyze_review_sentiments(text=review_obj.sentiment,version='2022-04-07',features='sentiment',return_analyzed_text=True)
            print(json.loads(review_obj.sentiment)['sentiment']['document']['label'])
            review_obj.sentiment = json.loads(review_obj.sentiment)['sentiment']['document']['label']
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(**kwargs):
# - Call get_request() with specified arguments
  url_watson = 'https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/bb000b33-495a-4b76-bcd1-a6d6620a66d6/v1/analyze'
  api_key_watson = 'QKiOdIghl0-40SqqJeRgM57bfHUJXR0NTBIFtYslRaJv'
  params = dict()
  params["text"] = kwargs["text"]
  params["version"] = kwargs["version"]
  params["features"] = kwargs["features"]
  params["return_analyzed_text"] = kwargs["return_analyzed_text"]
  print("authorization call stated for watson nlu...")
  print(url_watson)
  print(api_key_watson)
  print(params)
# Direct call
  response = requests.get(url_watson, headers={'Content-Type': 'application/json'}, params=params,
                                    auth=HTTPBasicAuth('apikey', api_key_watson))
  print(response.status_code)
  print(response.text)
  return response.text
# - Get the returned sentiment label such as Positive or Negative



