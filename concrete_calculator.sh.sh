#!/bin/bash


./concrete_calculator.py

echo "Job Summary"
sqlite3 jobs.db <<EOF
select * from jobs;
EOF

echo "Posts specifics"
sqlite3 jobs.db <<EOF
select * from posts;
EOF
