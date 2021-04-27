# Releasing grambank.clld.org

- recreate the database running
  ```shell
  clld initdb development.ini --cldf ../grambank-cldf/cldf/StructureDataset-metadata.json
  ```
- Run the tests
