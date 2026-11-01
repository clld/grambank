# Releasing grambank.clld.org

```shell
git clone https://github.com/clld/grambank
git clone --branch v1.0.3 --depth 1 https://github.com/grambank/grambank grambank-cldf
cd grambank
pip install -e .[test]
```

Recreate the database running
```shell
clld initdb development.ini --cldf ../grambank-cldf/cldf/StructureDataset-metadata.json
```

Run the tests
```shell
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO --compress gzip:9 grambank > grambank.sql.gz
```

