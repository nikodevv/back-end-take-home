## Installation


Requires Python 3.7

    // Clone repo
    git clone https://github.com/nikodevv/back-end-take-home gitlogix
    cd gitlogix
    // Create a virtual environment and install app requirements
    python -m pip install venv
    source venv/bin/activate
    pip install -r requirements.txt
    // Verify app is installed correctly
    pyhton manage.py test
    > Ran 22 tests in 0.244s - Ok


The database is committed to the repository for easier packaging, but additional csv data can be transformed and easily added to the database with the CLI command:

    python manage.py load_airports './path/to/airports.csv'
    python manage.py load_routes './path/to/routes.csv'

## API Example

Endpoint for finding routes ins `/api/v1/find_route?origin=<origin>&destination=<destination>`

Returns response containing the fastest route if there is a path avaialbe from origin to destination (status code 200)

Otherwise returns a meaningful error message (code 403 or 400)

    /api/v1/find_route?origin=SOF&destination=YYZ
    > SOF -> IST -> YYZ

A live demo of the web app can be found at: 
`http://35.202.181.185/api/v1/find_route?origin=YYZ&destination=SOF`


## Deployment

The server is manually deployed to an inexpensive** Google Cloud `Compute Engine` instance. The server is running `nginx` which is connected to a `gunicorn` web socket.
