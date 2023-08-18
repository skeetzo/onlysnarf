#/bin/bash
echo -n "Enter APP_KEY" 
read APP_KEY

echo -n "Enter APP_SECRET" 
read APP_SECRET
BASIC_AUTH=$(echo -n $APP_KEY:$APP_SECRET | base64)

echo "Navigate to URL and get ACCESS CODE"
echo "https://www.dropbox.com/oauth2/authorize?client_id=$APP_KEY&token_access_type=offline&response_type=code"

echo -n "Return to this script once you have the ACCESS_CODE" 
read DUMMY

echo -n "Enter the ACCESS_CODE" 
read ACCESS_CODE_GENERATED

curl --location --request POST 'https://api.dropboxapi.com/oauth2/token' \
--header "Authorization: Basic $BASIC_AUTH" \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode "code=$ACCESS_CODE_GENERATED" \
--data-urlencode 'grant_type=authorization_code'
