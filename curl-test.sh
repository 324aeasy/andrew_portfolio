#!/bin/bash

echo "Testing GET /api/timeline_post"
curl http://172.31.32.1:5000/api/timeline_post

echo "Testing POST /api/timeline_post"
curl -X POST http://172.31.32.1:5000/api/timeline_post -d \
'id=9001&name=Testy&email=testy@example.com&content=This is a test post'

echo "Testing GET /api/timeline_post"
curl http://172.31.32.1:5000/api/timeline_post

echo "Testing DELETE /api/timeline_post"
curl -X DELETE "http://172.31.32.1:5000/api/timeline_post?id=9001"

echo "Testing GET /api/timeline_post after deletion"
curl http://172.31.32.1:5000/api/timeline_post