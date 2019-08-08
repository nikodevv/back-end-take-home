# Installation

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

The database is committed to the repository for easier packaging, but additional csv data can be transformed and easily added to the database with the CLI command:

    python manage.py load_routes './path/to/routes.csv'
