# Releasing Polyglotta Africana

- Install the software
  ```shell
  git clone https://github.com/clld/polyglottaafricana
  cd polyglottaafricana
  pip install -e .[test]
  ```
- Check out the latest released version of the dataset
- Recreate the database:
  ```shell
  clld initdb --cldf ../polyglottaafricana-cldf/cldf/cldf-metadata.json --glottolog ../../glottolog/glottolog development.ini
  pytest
  ```
- Store the tested requirements:
  ```shell
  pip freeze > requirements.txt
  ```
- Store a db dump:
  ```shell
  pg_dump -xO polyglottaafricana > polyglottaafricana.sql
  zip polyglottaafricana.sql.zip polyglottaafricana.sql
  rm polyglottaafricana.sql
  ```
