# Pricemory
Tracking and display of price history of products from Paraguay

![project example](resources/img/project_example.png)

It uses scrapy for scraping shops sites and django for web framework

### Tracked shops
- [Superseis](https://www.superseis.com.py) 
- [Stock](https://www.stock.com.py)
- [Casa Rica](https://www.casarica.com.py/)
- [Nissei](https://www.casanissei.com)
- [Tupi](https://www.tupi.com.py/)
- [Los Jardines](https://losjardinesonline.com.py/)

 
## Requirements

- Python 3.6+
- Django 2.2+

## Installation

1. Clone and install project
```
git clone git@github.com:mauri-medina/pricemory.git
cd pricemory
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
./manage.py migrate

```

2. Configurations
- the existing values in .env can be used but is recommended to create a new secret key for django.

## Usage

### Run spiders
From the crawler directory:<br>
`scrapy crawl spider-name`

The spider names are specified in their files, for example to run the spider from super seis:<br>
`scrapy crawl superseis_spider`

This will save the scrapped data to the database, to save in another formats check [scrappy](https://docs.scrapy.org/en/latest/index.html) documentation

### Run django
`./manage.py runserver`

## Contributing
Pull requests are welcome.

Any help or feedback is appreciated, especially for the design of the site.

## TODO
- General improve of site design
- Add more shops
- Add a way to select more than one product to show chart history, the backend is already prepared for this


## License
This project is licensed under the terms of the GNU General Public License v3.0
