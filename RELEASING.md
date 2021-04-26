# Releasing grambank.clld.org

- pull latest changes from
  - glottobank/Grambank
  - glottobank/grambank-cldf
  - glottolog/glottolog
- recreate the database running
  ```shell
  clld initdb  --cldf ../grambank-cldf/cldf/StructureDataset-metadata.json --glottolog-version=v...
  ```
- Run the tests
