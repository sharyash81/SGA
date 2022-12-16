#!/bin/bash

db_name=$1

echo "***** start mongodb service *****"
systemctl start mongod
./sqlite2Json.sh "database.sqlite"
python3 data_cleaner.py

echo "***** DB Creation process starts *****"
rm -rf 'jsonCols/Team_Attributes.json'
mongosh --eval "use '${db_name}'"
for clc in $( ls jsonCols);do
	mongoimport --db $db_name --collection ${clc%.*} --file ./jsonCols/$clc --jsonArray
done
