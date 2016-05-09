SET PGPASSWORD=blodig1kuk
dropdb -U postgres grambank
createdb -U postgres grambank
REM psql -U postgres -f pldb.sql linc
..\python grambank/scripts/initializedb.py development.ini --module grambank
REM > ntserr.log
pserve --reload development.ini
