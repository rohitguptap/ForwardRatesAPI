## Forward Curve Rate Service

## Deliverables
The project contains 2 main components:
* An ETL job to extract the 1-Month SOFR forward rates from  https://www.pensford.com/resources/forward-curve and save the results in sqlite db. 
* A FastAPI service running to listen to the request from clients, it returns date along with its corresponding rate based on ceiling/floor/spread provided in the request. It sends the response in an json object
* It took around 4 hours to complete project.



### Libraries used
* FastAPI
* Selenium
* Sqlite
* Python 3.9


## Getting Started
Clone this project to your local machine

### Installation
Run pip install to install all the dependencies
```
pip install -r requirements.txt
```

### ETL Job
* To Run the etl job, simply navigate to project root folder and execute the following python file:
```
python forward_rates_etl.py
```
 * The job extracts latest curve rate from website (https://www.pensford.com/resources/forward-curve), inserts the rates into the Sqlite ForwardCurve table 


 ### Forward Rate API
 *  Run the following file:
 ```
 python forward_rate_api.py
 ```
Forward Rates API:
The POST API takes the maturity date, reference_rate, rate_floor, rate_ceiling & rate_spread 
and uses the closest day available in database against this maturity date in a month and display all curve rates up to this maturity date.


```bash
curl -X POST "http://localhost:8000/forward_rates/" \
-H "Content-Type: application/json" \
-d '{ "maturity_date": "2025-02-01", "reference_rate": "SOFR", "rate_floor": 0.02, "rate_ceiling": 0.10, "rate_spread": 0.02 }'
 ```
Response:

[{"date":"2024-11-04","rate":0.0664},{"date":"2024-12-04","rate":0.0651},{"date":"2025-01-06","rate":0.0638}]


## Improvements

1. Add Rate Limiting and Input Validation
2.  Implement OAuth2 / JWT Authentication
3.  Automate ETL with a scheduler (e.g., cron or Celery) to keep data consistently updated.
4.  Pagination for Large Data Sets
5.  Use Swagger/OpenAPI to document endpoints, request, and response
6.   Add health check endpoints and use Prometheus/Grafana for real-time system monitoring.
7. Set up automated testing and deployment with a CI/CD pipeline
8. Use environment variables for settings like database URLs and secrets.
9. Add UI for forward rate trends, enhancing data comprehension for users.
10.  Use caching (e.g., Redis or in memory) for frequently requested data to reduce load and improve response times. 



