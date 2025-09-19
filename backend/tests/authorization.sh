#!/bin/bash
set -euo pipefail

API_URL="http://localhost:8000"

source ../backend/tests/common_functions.sh

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
