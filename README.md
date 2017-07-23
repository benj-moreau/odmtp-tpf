# ODMTriP TPF Server

odmtrip-tpf is a Triple Pattern Fragment server using Python, Django and ODMTriP.

ODMTriP (On Demand Mapper with Triple pattern matching) enables triple pattern matching over non-RDF datasources.


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
From `~/odmtrip-tpf` run the comand:
```bash
python manage.py runserver
```

The TPF server should run at: http://127.0.0.1:8000/

#### Exemple
You can use any Triple Pattern Fragment client: http://linkeddatafragments.org/software/
to run SPARQL queries over twitter (https://dev.twitter.com/rest/public/search)

For exemple you can run this SPARQL querie over http://127.0.0.1:8000/ to retrieve tweets using #iswc2017 hashtag.
```sparql
PREFIX schema: <http://schema.org/> 
PREFIX it: <http://www.influencetracker.com/ontology#>

SELECT ?s WHERE {
 ?s <http://www.influencetracker.com/ontology#includedHashtag> "iswc2017".
}
```
