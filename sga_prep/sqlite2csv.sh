#!/bin/bash
file=$1
for table in $(sqlite3 $file '.tables');do
	sqlite3 $file '.mode csv' ".once $table.csv" "select * from $table"
done;
