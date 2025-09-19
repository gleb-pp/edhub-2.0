#!/bin/bash
set -euo pipefail

API_URL="http://localhost:8000"

source ./backend/tests/common_functions.sh

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
  "$API_URL/get_user_role?course_id=$mathcourseid")

expected='
  {"is_instructor":true,"is_teacher":true,"is_student":false,"is_parent":false,"is_admin":false}
'

json_exact_match_test "Get the Alice's role in course Math" "$info" "$expected" "is_instructor"

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

info=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_user_role?course_id=$engcourseid")

expected='
  {"is_instructor":true,"is_teacher":true,"is_student":false,"is_parent":false,"is_admin":false}
'

json_exact_match_test "Get the Bob's role in course English" "$info" "$expected" "is_instructor"

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

info=$(curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "$API_URL/get_user_role?course_id=$engcourseid")

expected='
  {"is_instructor":false,"is_teacher":false,"is_student":true,"is_parent":false,"is_admin":false}
'

json_exact_match_test "Get the Alice's role in course English" "$info" "$expected" "is_instructor"

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
