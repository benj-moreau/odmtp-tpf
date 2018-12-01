# ODMTP TPF Server
odmtp-tpf is a Triple Pattern Fragment server using Python, Django and ODMTP.

ODMTP (On Demand Mapper with Triple pattern matching) enables triple pattern matching over non-RDF datasources.

ODMTP support inference (see Semantic Reasoner (Inference) section)

# Online demo

ODMTP's implemented for Twitter API, Github API and Linkedin API are available online. You can run SPARQL queries using the online TPF client demo: [Here](http://client.linkeddatafragments.org/#datasources=http%3A%2F%2Fodmtp.priloo.univ-nantes.fr%2Ftwitter%2F&query=PREFIX%20it%3A%20%3Chttp%3A%2F%2Fwww.influencetracker.com%2Fontology%23%3E%0A%0ASELECT%20%3Fs%20WHERE%20%7B%0A%20%7B%3Fs%20it%3AincludedHashtag%20%22ISWC2018%22.%7D%20UNION%20%7B%3Fs%20it%3AincludedHashtag%20%22iswc2018%22.%7D%0A%7D) for Twitter,  [Here](http://client.linkeddatafragments.org/#datasources=http%3A%2F%2Fodmtp.priloo.univ-nantes.fr%2Fgithub%2F&query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0A%0ASELECT%20%3Frepo%0AWHERE%20%7B%0A%3Frepo%20schema%3Alanguage%20%22Java%22%0A%7D) for Github (limited to 60 request per hour) and [Here](http://odmtp.priloo.univ-nantes.fr/linkedin/authentification/) for your Linkedin profile (you will need to login to access your personal LI profile).

ODMTP approach is already used on [OpenDataSoft Plateform](https://data.opendatasoft.com) and can be tested [Here](http://client.linkeddatafragments.org/#datasources=https%3A%2F%2Fpublic.opendatasoft.com%2Fapi%2Ftpf%2Froman-emperors%2F&query=PREFIX%20roman%3A%20%3Chttps%3A%2F%2Fpublic.opendatasoft.com%2Fld%2Fontologies%2Froman-emperors%2F%3E%0A%0ASELECT%20%3Fname%20WHERE%20%7B%0A%20%20%3Fs%20roman%3Abirth_cty%20%22Rome%22%5E%5Exsd%3Astring%20.%0A%20%20%3Fs%20roman%3Areign_start%20%3Fdate%20.%0A%20%20%20%20FILTER%20(%3Fdate%20%3E%20%220014-12-31T00%3A00%3A00%2B00%3A00%22%5E%5Exsd%3AdateTime)%0A%20%20%3Fs%20%20roman%3Aname%20%3Fname%20.%0A%7D).

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

# Semantic Reasoner (Inference)
To support inference, ODMTP use ontologies to materialize implicite triples of mappings.
Each API can be queried using extended mappings at: `http://127.0.0.1:8000/{api}/extended`
Example: http://127.0.0.1:8000/twitter/extended

# Mappings
Mappings are accessible at: `http://127.0.0.1:8000/{api}/mapping`
Example: http://127.0.0.1:8000/twitter/mapping

Extended mapping are accessible at `http://127.0.0.1:8000/{api}/mapping/extended`
Example: http://127.0.0.1:8000/twitter/mapping/extended

# Examples of Simple Queries
You can use any Triple Pattern Fragment client: http://linkeddatafragments.org/software/
to run SPARQL queries over twitter API and github Repo API V3
## SPARQL queries over Twitter API
You can run this SPARQL query over http://127.0.0.1:8000/twitter/ to retrieve tweets using #iswc2017 hashtag.
```sparql
PREFIX it: <http://www.influencetracker.com/ontology#>

SELECT ?s WHERE {
 ?s it:includedHashtag "SemanticWeb".
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

# Extras
To understand how ODTMP approach is working, the ISWC 2017 poster is available [here](https://docs.google.com/presentation/d/e/2PACX-1vT7fstdxp9LrqPdYpVpbDopBjBLJB5oUysFDp8iS3Z33MCqk-6Yq-2OrWZuWT1tqyFWLeAYcv2kshXe/embed?).

This is just a prototype, feel free to optimize it, improve mapping files, work on new api's etc.
