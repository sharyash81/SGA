#!/bin/bash

mkdir jsonCols
file=$1
for table in $(sqlite3 $file '.tables');do
	sqlite3 $file '.mode json' ".once ./jsonCols/$table.json" "select * from $table"
done;
