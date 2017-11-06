# ODMTP TPF Server
odmtp-tpf is a Triple Pattern Fragment server using Python, Django and ODMTP.

ODMTP (On Demand Mapper with Triple pattern matching) enables triple pattern matching over non-RDF datasources.

# Online demo

ODMTP's implemented for Twitter API & Github API are available on herokuapp. You can run SPARQL queries using the online TPF client demo: [Here](http://client.linkeddatafragments.org/#datasources=https%3A%2F%2Fodmtp.herokuapp.com%2Ftwitter%2F&query=PREFIX%20it%3A%20%3Chttp%3A%2F%2Fwww.influencetracker.com%2Fontology%23%3E%0A%0ASELECT%20%3Fs%20WHERE%20%7B%0A%20%7B%3Fs%20it%3AincludedHashtag%20%22ISWC2017%22.%7D%20UNION%20%7B%3Fs%20it%3AincludedHashtag%20%22iswc2017%22.%7D%0A%7D) for Twitter and [Here](http://client.linkeddatafragments.org/#datasources=https%3A%2F%2Fodmtp.herokuapp.com%2Fgithub%2F&query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0A%0ASELECT%20%3Frepo%0AWHERE%20%7B%0A%3Frepo%20schema%3Alanguage%20%22Java%22%0A%7D) for Github (limited to 60 request per hour).

# Instructions
## Prelude

#### macOS
You need to install [Homebrew](http://brew.sh/).

and then install Python 2.7:
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

# Examples of Simple Queries
You can use any Triple Pattern Fragment client: http://linkeddatafragments.org/software/
to run SPARQL queries over twitter API and github Repo API V3
## SPARQL queries over Twitter API
You can run this SPARQL query over http://127.0.0.1:8000/twitter/ to retrieve tweets using #iswc2017 hashtag.
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

## SPARQL queries over Github API
You can run this SPARQL query over http://127.0.0.1:8000/github/ to retrieve repositories using Java programming language.
```sparql
PREFIX schema: <http://schema.org/>

SELECT ?repo
WHERE {
?repo schema:language "Java"
}
```

SPO query to browse repositories
```sparql
SELECT ?s ?p ?o WHERE {
 ?s ?p ?o
}
```
