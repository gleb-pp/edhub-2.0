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
    local sort_fields_str="${4:-}"

    IFS=' ' read -r -a sort_fields <<< "$sort_fields_str"

    local jq_sort_key=""
    if [ ${#sort_fields[@]} -gt 0 ] && [ -n "${sort_fields[0]}" ]; then
        jq_sort_key="["
        local first=1
        for field in "${sort_fields[@]}"; do
            if [ $first -eq 1 ]; then
                jq_sort_key+=".${field}"
                first=0
            else
                jq_sort_key+=", .${field}"
            fi
        done
        jq_sort_key+="]"
    fi

    local jq_prog='(if type=="array" then . else [.] end)'
    if [ -n "$jq_sort_key" ]; then
        jq_prog+=' | sort_by('"$jq_sort_key"')'
    fi

    local sorted_response
    sorted_response=$(echo "$json_response" | jq -S "$jq_prog")
    local sorted_expected
    sorted_expected=$(echo "$expected_json" | jq -S "$jq_prog")

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

json_partial_match_test() {
    local name="$1"
    local json_response="$2"
    local expected_json="$3"
    local sort_fields_str="${4:-}"
    local ignore_fields_str="${5:-}"

    IFS=' ' read -r -a sort_fields <<< "$sort_fields_str"
    IFS=' ' read -r -a ignore_fields <<< "$ignore_fields_str"

    local jq_sort_key=""
    if [ ${#sort_fields[@]} -gt 0 ] && [ -n "${sort_fields[0]}" ]; then
        jq_sort_key="["
        local first=1
        for field in "${sort_fields[@]}"; do
            if [ $first -eq 1 ]; then
                jq_sort_key+=".${field}"
                first=0
            else
                jq_sort_key+=", .${field}"
            fi
        done
        jq_sort_key+="]"
    fi

    local jq_del_args=""
    if [ ${#ignore_fields[@]} -gt 0 ] && [ -n "${ignore_fields[0]}" ]; then
        local first=1
        for field in "${ignore_fields[@]}"; do
            if [ $first -eq 1 ]; then
                jq_del_args+=".${field}"
                first=0
            else
                jq_del_args+=", .${field}"
            fi
        done
    fi

    local jq_prog='(if type=="array" then . else [.] end)'
    if [ -n "$jq_sort_key" ]; then
        jq_prog+=' | sort_by('"$jq_sort_key"')'
    fi
    if [ -n "$jq_del_args" ]; then
        jq_prog+=' | map(del('"$jq_del_args"'))'
    fi

    local filtered_response
    filtered_response=$(echo "$json_response" | jq -S "$jq_prog")
    local filtered_expected
    filtered_expected=$(echo "$expected_json" | jq -S "$jq_prog")

    if [ "$filtered_response" = "$filtered_expected" ]; then
        echo "✓ Successful $name"
    else
        echo "ERROR: $name failed"
        echo "Expected (sorted & ignored fields removed):"
        echo "$filtered_expected"
        echo "Received (sorted & ignored fields removed):"
        echo "$filtered_response"
        exit 1
    fi
}

extract_field() {
    local field="$1"
    python3 -c "import sys, json; print(json.load(sys.stdin).get('$field', ''))"
}

# --------------------------------------------------------------------

success_test "Registration of Alice" \
    -X POST $API_URL/create_user \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"alicePass123!\",\"name\":\"Alice\"}"

# --------------------------------------------------------------------

success_test "Registration of Bob" \
    -X POST $API_URL/create_user \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"bob@example.com\",\"password\":\"bobPass123!\",\"name\":\"Bob\"}"

# --------------------------------------------------------------------

login_and_get_token "Login as Alice" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"alicePass123!\"}"

# --------------------------------------------------------------------

mathcourseid=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/create_course?title=Math&organization=Innopolis%20University" | extract_field course_id)

# --------------------------------------------------------------------

info=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_course_info?course_id=$mathcourseid")

expected='[
  {"course_id":"'"$mathcourseid"'","title":"Math","instructor":"alice@example.com","organization":"Innopolis University"}
]'

json_partial_match_test "Request the course info from Alice" "$info" "$expected" "course_id" "creation_time"

# --------------------------------------------------------------------

materialid=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/create_material?course_id=$mathcourseid&title=Lecture%20material&description=Lecture%20material%20describtion" | extract_field material_id)

# --------------------------------------------------------------------

assignmentid=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/create_assignment?course_id=$mathcourseid&title=Assignment%201&description=To%20do%20exercise%2010%20from%20the%20course%20book" | extract_field assignment_id)

# --------------------------------------------------------------------

info=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_course_feed?course_id=$mathcourseid")

expected='[
  {"course_id":"'"$mathcourseid"'","post_id":'$materialid',"type":"mat","author":"alice@example.com"},
  {"course_id":"'"$mathcourseid"'","post_id":'$assignmentid',"type":"ass","author":"alice@example.com"}
]'

json_partial_match_test "Request the course feed from Alice" "$info" "$expected" "post_id type" "timeadded"

# --------------------------------------------------------------------

info=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_material?course_id=$mathcourseid&material_id=$materialid")

expected='
  {"course_id":"'"$mathcourseid"'","material_id":'$materialid',"title":"Lecture material","description":"Lecture material describtion","author":"alice@example.com"}
'

json_partial_match_test "Request the material info from Alice" "$info" "$expected" "material_id" "creation_time"

# --------------------------------------------------------------------

info=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_assignment?course_id=$mathcourseid&assignment_id=$assignmentid")

expected='
  {"course_id":"'"$mathcourseid"'","assignment_id":'$assignmentid',"title":"Assignment 1","description":"To do exercise 10 from the course book","author":"alice@example.com"}
'

json_partial_match_test "Request the assignment info from Alice" "$info" "$expected" "assignment_id" "creation_time"

# --------------------------------------------------------------------

login_and_get_token "Login as Bob" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"bob@example.com\",\"password\":\"bobPass123!\"}"

# --------------------------------------------------------------------

courses=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/available_courses")

expected='[]'

json_exact_match_test "Request the list of available courses from Bob" "$courses" "$expected" "course_id"

# --------------------------------------------------------------------

courses=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_instructor_courses")

expected='[]'

json_exact_match_test "Request the list of instructor courses from Bob" "$courses" "$expected" "course_id"

# --------------------------------------------------------------------

fail_test "Request the course info from Bob" \
    -X GET "$API_URL/get_course_info?course_id=$mathcourseid" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

fail_test "Request the course feed from Bob" \
    -X GET "$API_URL/get_course_feed?course_id=$mathcourseid" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

fail_test "Request the course material from Bob" \
    -X GET "$API_URL/get_material?course_id=$mathcourseid&material_id=$materialid" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

fail_test "Request the course assignment from Bob" \
    -X GET "$API_URL/get_assignment?course_id=$mathcourseid&assignment_id=$assignmentid" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

engcourseid=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/create_course?title=English&organization=Skyeng" | extract_field course_id)

# --------------------------------------------------------------------

success_test "Invite Alice to Bob's course" \
    -X POST "$API_URL/invite_student?course_id=$engcourseid&student_email=alice@example.com" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

materialid=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/create_material?course_id=$engcourseid&title=Lecture%20material&description=Lecture%20material%20describtion" | extract_field material_id)

# --------------------------------------------------------------------

assignmentid=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/create_assignment?course_id=$engcourseid&title=Assignment%201&description=To%20do%20exercise%2010%20from%20the%20course%20book" | extract_field assignment_id)

# --------------------------------------------------------------------

login_and_get_token "Login as Alice" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"alicePass123!\"}"

# --------------------------------------------------------------------

courses=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/available_courses")

expected='[
    {"course_id":"'"$mathcourseid"'"},
    {"course_id":"'"$engcourseid"'"}
]'

json_exact_match_test "Request the list of available courses from Alice" "$courses" "$expected" "course_id"

# --------------------------------------------------------------------

courses=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_instructor_courses")

expected='[
    {"course_id":"'"$mathcourseid"'"}
]'

json_exact_match_test "Request the list of instructor courses from Alice" "$courses" "$expected" "course_id"

# --------------------------------------------------------------------

info=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_course_feed?course_id=$engcourseid")

expected='[
  {"course_id":"'"$engcourseid"'","post_id":'$materialid',"type":"mat","author":"bob@example.com"},
  {"course_id":"'"$engcourseid"'","post_id":'$assignmentid',"type":"ass","author":"bob@example.com"}
]'

json_partial_match_test "Request the course feed from Alice" "$info" "$expected" "post_id type" "timeadded"

# --------------------------------------------------------------------

info=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_material?course_id=$engcourseid&material_id=$materialid")

expected='
  {"course_id":"'"$engcourseid"'","material_id":'$materialid',"title":"Lecture material","description":"Lecture material describtion","author":"bob@example.com"}
'

json_partial_match_test "Request the material info from Alice" "$info" "$expected" "material_id" "creation_time"

# --------------------------------------------------------------------

info=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_assignment?course_id=$engcourseid&assignment_id=$assignmentid")

expected='
  {"course_id":"'"$engcourseid"'","assignment_id":'$assignmentid',"title":"Assignment 1","description":"To do exercise 10 from the course book","author":"bob@example.com"}
'

json_partial_match_test "Request the assignment info from Alice" "$info" "$expected" "assignment_id" "creation_time"

# --------------------------------------------------------------------

fail_test "Request to delete Bob's course from Alice" \
    -X POST "$API_URL/remove_course?course_id=$engcourseid" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

login_and_get_token "Login as Bob" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"bob@example.com\",\"password\":\"bobPass123!\"}"

# --------------------------------------------------------------------

success_test "Delete Bob's course" \
    -X POST "$API_URL/remove_course?course_id=$engcourseid" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

login_and_get_token "Login as Alice" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"alicePass123!\"}"

# --------------------------------------------------------------------

courses=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/available_courses")

expected='[
    {"course_id":"'"$mathcourseid"'"}
]'

json_exact_match_test "Request the list of available courses from Alice" "$courses" "$expected" "course_id"

# --------------------------------------------------------------------

fail_test "Request to get the feed of the removed course" \
    -X GET "$API_URL/get_course_feed?course_id=$engcourseid" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

fail_test "Request to get the material of the removed course" \
    -X GET "$API_URL/get_material?course_id=$engcourseid&material_id=$materialid" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

fail_test "Request to get the assignment of the removed course" \
    -X GET "$API_URL/get_assignment?course_id=$engcourseid&assignment_id=$assignmentid" \
    -H "Authorization: Bearer $TOKEN" \