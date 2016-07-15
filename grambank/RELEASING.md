
Releasing grambank
==================

- Update the glottobank/Grambank repository
- Run the checks on the data repos:
```
grambank check
```
- Recreate the database
- Recompute coverage information running
```
cd grambank/coverage
./coverage.sh
```
- Run the tests
