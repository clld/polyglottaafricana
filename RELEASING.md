# Releasing Polyglotta Africana

Install the software
```shell
git clone https://github.com/clld/polyglottaafricana
git clone --branch v2.2 --depth 1 https://github.com/lexibank/polyglottaafricana polyglottaafricana-cldf
git clone --branch v2.3.1 --depth 1 https://github.com/cldf-clts/clts
git clone --branch v5.3 --depth 1 https://github.com/glottolog/glottolog
cd polyglottaafricana
pip install -e .[test]
```
Check out the latest released version of the dataset
Recreate the database:
```shell
clld initdb --cldf ../polyglottaafricana-cldf/cldf/cldf-metadata.json --glottolog ../glottolog development.ini
pytest
```
Store the tested requirements:
```shell
pip freeze > requirements.txt
```
Store a db dump:
```shell
pg_dump -xO --compress gzip:9 polyglottaafricana > polyglottaafricana.sql.gz
```
