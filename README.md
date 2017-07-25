# ODMTP TPF Server

odmtp-tpf is a Triple Pattern Fragment server using Python, Django and ODMTP.

ODMTP (On Demand Mapper with Triple pattern matching) enables triple pattern matching over non-RDF datasources.


# Instructions
## Prelude

#### macOS
You need to install [Homebrew](http://brew.sh/).

and then install Python:
```bash
brew install python
```
#### Ubuntu
```
sudo apt-get install python-dev python-setuptools
```

## Dependencies
You need to install dependencies with pip:
```bash
pip install -r requirements.txt
```

## Running The Platform
#### macOS & Ubuntu
From `~/odmtp-tpf` run the comand:
```bash
python manage.py runserver
```

The TPF server should run at: http://127.0.0.1:8000/

#### Exemple
You can use any Triple Pattern Fragment client: http://linkeddatafragments.org/software/
to run SPARQL queries over twitter (https://dev.twitter.com/rest/public/search)

For exemple you can run this SPARQL query over http://127.0.0.1:8000/ to retrieve tweets using #iswc2017 hashtag.
```sparql
PREFIX it: <http://www.influencetracker.com/ontology#>

SELECT ?s WHERE {
 {?s it:includedHashtag "ISWC2017".} UNION {?s it:includedHashtag "iswc2017".}
}
```

Retrieve tweets from a specific user.
```sparql
PREFIX schema: <http://schema.org/>

SELECT ?s WHERE {
 ?s schema:author "NantesTech".
}
```

SPO query to browse tweets
```sparql
SELECT ?s ?p ?o WHERE {
 ?s ?p ?o
}
```

To retrieve a specific tweet by ID
```sparql
SELECT ?p ?o WHERE {
 <https://twitter.com/statuses/889775221452005377> ?p ?o
}
```


