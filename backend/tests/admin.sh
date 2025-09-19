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

json_exact_match_test() {
    local name="$1"
    local json_response="$2"
    local expected_json="$3"
    local sort_field="$4"

    local sorted_response
    local sorted_expected

    sorted_response=$(echo "$json_response" | jq --sort-keys "sort_by(.$sort_field)")
    sorted_expected=$(echo "$expected_json" | jq --sort-keys "sort_by(.$sort_field)")

    if [ "$sorted_response" = "$sorted_expected" ]; then
        echo "✓ Successful $name"
    else
        echo "ERROR: $name failed."
        echo "Expected:"
        echo "$sorted_expected"
        echo "Received:"
        echo "$sorted_response"
        exit 1
    fi
}

# --------------------------------------------------------------------

success_test "Registration of Alice" \
    -X POST $API_URL/create_user \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"alicePass123!\",\"name\":\"Alice\"}"

# --------------------------------------------------------------------

login_and_get_token "Login as Alice" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"alicePass123!\"}"

# --------------------------------------------------------------------

fail_test "Request the list of all users from Alice" \
    -X GET "$API_URL/get_all_users" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

fail_test "Request the list of all courses from Alice" \
    -X GET "$API_URL/get_all_courses" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

admins=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_admins")

expected='[
  {"email":"admin","name":"admin"}
]'

json_exact_match_test "Request the list of admins from Alice" "$admins" "$expected" "email"

# --------------------------------------------------------------------

login_and_get_token "Login as Admin" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"admin\",\"password\":\"admin\"}"

# --------------------------------------------------------------------

users=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_all_users")

expected='[
  {"email":"admin","name":"admin"},
  {"email":"alice@example.com","name":"Alice"}
]'

json_exact_match_test "Request the list of all users from Admin" "$users" "$expected" "email"

# --------------------------------------------------------------------

admins=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_admins")

expected='[
  {"email":"admin","name":"admin"}
]'

json_exact_match_test "Request the list of admins from Admin" "$admins" "$expected" "email"

# --------------------------------------------------------------------

courses=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_all_courses")

expected='[]'

json_exact_match_test "Request the list of courses from Admin" "$courses" "$expected" "course_id"

# --------------------------------------------------------------------

success_test "Giving admin rights to Alice by Admin" \
    -X POST "$API_URL/give_admin_permissions?object_email=alice@example.com" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

success_test "Giving admin rights to Alice by Admin" \
    -X POST "$API_URL/give_admin_permissions?object_email=alice@example.com" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

success_test "Removing Alice account from Admin" \
    -X POST "$API_URL/remove_user?deleted_user_email=alice@example.com" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------
