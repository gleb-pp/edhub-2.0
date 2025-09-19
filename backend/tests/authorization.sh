#!/bin/bash
set -euo pipefail

API_URL="http://localhost:8000"

get_http_code() {
    curl -s -o /dev/null -w "%{http_code}" "$@"
}

success_test() {
    local name="$1"
    shift
    local http_code
    http_code=$(get_http_code "$@")
    if [ "$http_code" -eq 200 ]; then
        echo "✓ Successful $name"
    else
        echo "ERROR: $name failed with HTTP $http_code"
        exit 1
    fi
}

fail_test() {
    local name="$1"
    shift
    local http_code
    http_code=$(get_http_code "$@")
    if [ "$http_code" -ge 400 ]; then
        echo "✓ Successfully rejected $name"
    else
        echo "ERROR: $name expected to fail, but got HTTP $http_code"
        exit 1
    fi
}

login_and_get_token() {
    local name="$1"; shift
    local body="/tmp/login_body.json"
    local code
    code=$(curl -sS -o "$body" -w "%{http_code}" "$@")
    if [[ "$code" =~ ^[0-9]{3}$ ]] && [ "$code" -ge 200 ] && [ "$code" -lt 300 ]; then
    echo "✓ Successful $name"
    TOKEN=$(python3 -c 'import sys,json; print(json.load(open(sys.argv[1])).get("access_token",""))' "$body")
    if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
        echo "ERROR: $name did not return a valid token"
        head -c 500 "$body" || true
        exit 1
    else
        echo "✓ Extracted token: $TOKEN"
    fi
    else
    echo "ERROR: $name failed with HTTP $code"
    head -c 500 "$body" || true
    exit 1
    fi
}

fail_test "Registration with incorrect email" \
  -X POST "$API_URL/create_user" \
  -H "Content-Type: application/json" \
  -d '{"email":"mailmail","password":"Password123!","name":"Alice"}'

fail_test "Registation with weak password" \
    -X POST $API_URL/create_user \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"pwd\",\"name\":\"Alice\"}"

success_test "Correct registration of Alice" \
    -X POST $API_URL/create_user \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"alicePass123!\",\"name\":\"Alice\"}"

fail_test "Registration with existing email" \
    -X POST $API_URL/create_user \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"Password123!\",\"name\":\"Bob\"}"

fail_test "Login with non-existing email" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"randomemail@example.com\",\"password\":\"Password123!\"}"

fail_test "Login with incorrect password" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"Password123!\"}"

login_and_get_token "Correct login as Alice" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"alicePass123!\"}"

fail_test "Changing password with incorrect original password" \
    -X POST "$API_URL/change_password" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"Password123!\",\"new_password\":\"NewPass456!\"}"

success_test "Correct changing password" \
    -X POST "$API_URL/change_password" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"alicePass123!\",\"new_password\":\"AlicePass123!\"}"

success_test "Correct registration of Bob" \
    -X POST $API_URL/create_user \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"bob@example.com\",\"password\":\"bobPass123!\",\"name\":\"Bob\"}"

fail_test "Removing Bob account from Alice" \
    -X POST "$API_URL/remove_user?deleted_user_email=bob@example.com" \
    -H "Authorization: Bearer $TOKEN" \

success_test "Removing Alice account from Alice" \
    -X POST "$API_URL/remove_user?deleted_user_email=alice@example.com" \
    -H "Authorization: Bearer $TOKEN" \

login_and_get_token "Correct login as Bob" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"bob@example.com\",\"password\":\"bobPass123!\"}"

success_test "Removing Bob account from Bob" \
    -X POST "$API_URL/remove_user?deleted_user_email=bob@example.com" \
    -H "Authorization: Bearer $TOKEN" \
