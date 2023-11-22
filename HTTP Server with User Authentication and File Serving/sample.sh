SERVER_IP="127.0.0.1"
SERVER_PORT="8081"

# Variables for storing session cookies
SESSION_COOKIE=""

# Common curl options for HTTP/1.0 and connection close
CURL_OPTIONS="--http1.0 --connect-timeout 5 --max-time 10 --fail --silent"

SESSION_COOKIE=$(curl -i -v -X POST -H "password: 3TQI8TB39DFIMI6" "http://${SERVER_IP}:${SERVER_PORT}/" | grep -i 'Set-Cookie' | cut -d ' ' -f 2 | cut -d '=' -f 2)

SESSION_COOKIE=$(curl -i -v -X POST -H "username: Richard" "http://${SERVER_IP}:${SERVER_PORT}/" | grep -i 'Set-Cookie' | cut -d ' ' -f 2 | cut -d '=' -f 2)

SESSION_COOKIE=$(curl -i -v -X POST -H "username: Angela" -H "password: 3TQI8TB39DFIMI6" "http://${SERVER_IP}:${SERVER_PORT}/" | grep -i 'Set-Cookie' | cut -d ' ' -f 2 | cut -d '=' -f 2)

SESSION_COOKIE=$(curl -i -v -X POST -H "username: Richard" -H "password: XMLU8ZPD7Z9BMC5" "http://${SERVER_IP}:${SERVER_PORT}/" | grep -i 'Set-Cookie' | cut -d ' ' -f 2 | cut -d '=' -f 2)

SESSION_COOKIE=$(curl -i -v -X POST -H "username: Richard" -H "password: 3TQI8TB39DFIMI6" "http://${SERVER_IP}:${SERVER_PORT}/" | grep -i 'Set-Cookie' | cut -d ' ' -f 2 | cut -d '=' -f 2)

SESSION_COOKIE=$(curl -i -v -X POST -H "username: Richard" -H "password: 3TQI8TB39DFIMI6" "http://${SERVER_IP}:${SERVER_PORT}/" | grep -i 'Set-Cookie' | cut -d ' ' -f 2 | cut -d '=' -f 2)

curl $CURL_OPTIONS -v -X GET -H "Cookie: sessionID=apple" "http://${SERVER_IP}:${SERVER_PORT}/file.txt"

curl $CURL_OPTIONS -v -X GET -H "Cookie: sessionID=$SESSION_COOKIE" "http://${SERVER_IP}:${SERVER_PORT}/file.txt"

SESSION_COOKIE=$(curl -i -v -X POST -H "username: Angela" -H "password: XMLU8ZPD7Z9BMC5" "http://${SERVER_IP}:${SERVER_PORT}/" | grep -i 'Set-Cookie' | cut -d ' ' -f 2 | cut -d '=' -f 2)

curl $CURL_OPTIONS -v -X GET -H "Cookie: sessionID=$SESSION_COOKIE" "http://${SERVER_IP}:${SERVER_PORT}/file.txt"

curl $CURL_OPTIONS -v -X GET -H "Cookie: sessionID=$SESSION_COOKIE" "http://${SERVER_IP}:${SERVER_PORT}/file2.txt"

sleep 6s

curl $CURL_OPTIONS -v -X GET -H "Cookie: sessionID=$SESSION_COOKIE" "http://${SERVER_IP}:${SERVER_PORT}/file.txt"
