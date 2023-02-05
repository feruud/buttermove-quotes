
# ButterMove Quotes microservice
This is a microservice used to create quotes for a ButterMove trip.

## Pre-requisites

- Python 3.0+
- Pip 3
- virtualenv

## Get Started

1. Clone this repository
2. Activate venv with the following command
````
$ source venv/bin/activate
````
3. Install requirements (if needed)
````
$ pip3 install -r requirements.txt
````
4. Init database and run migrations
````
$ python3 buttermove_quotes.py db init
$ python3 buttermove_quotes.py db migrate
$ python3 buttermove_quotes.py db upgrade
````
5. Seed the database
````
$ python3 buttermove_quotes.py seed
````
6. Run microservice
````
$ python3 buttermove_quotes.py run
````

## Testing

This microservice comes with several test cases,
in order to test the application just execute
````
$ python3 buttermove_quotes.py test
````

## API reference

Once you run the application there will be a 
Swagger API available at

````
http://127.0.0.1:5000/
````

and here's an example of a successfull call as well

````
curl --location --request POST '0.0.0.0:5000/quote/' \
    --header 'ip-client: 127.0.0.1' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "state_code": "TX",
        "quote_type": "PREMIUM",
        "trip_distance_km": 31,
        "base_fare_usd": 123
    }'  
````