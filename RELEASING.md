# Releasing grambank.clld.org

```shell
git clone https://github.com/clld/grambank
git clone https://github.com/grambank/grambank grambank-cldf
git -C grambank-cldf checkout v1.0.3
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
pg_dump -xO grambank > grambank.sql
zip grambank.sql.zip grambank.sql
rm grambank.sql
```

