# Releasing grambank.clld.org

- pull latest changes from
  - glottobank/Grambank
  - glottobank/grambank-cldf
  - glottolog/glottolog
- recreate the database running
```shell script
grambank-app initdb --glottolog-version=v...
```
- Run the tests
