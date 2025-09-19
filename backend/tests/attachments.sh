#!/bin/bash
set -euo pipefail

API_URL="http://localhost:8000"

source ./backend/tests/common_functions.sh

# --------------------------------------------------------------------

success_test "Registration of Alice" \
    -X POST $API_URL/create_user \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"alice@example.com\",\"password\":\"alicePass123!\",\"name\":\"Alice\"}"

success_test "Registration of Bob" \
    -X POST $API_URL/create_user \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"bob@example.com\",\"password\":\"bobPass123!\",\"name\":\"Bob\"}"

success_test "Registration of Charlie" \
    -X POST $API_URL/create_user \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"charlie@example.com\",\"password\":\"charliePass123!\",\"name\":\"Charlie\"}"

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

success_test "Invite Bob to Alice's course as a student" \
    -X POST "$API_URL/invite_student?course_id=$mathcourseid&student_email=bob@example.com" \
    -H "Authorization: Bearer $TOKEN" \

success_test "Invite Charlie to Alice's course as Bob's parent" \
    -X POST "$API_URL/invite_parent?course_id=$mathcourseid&student_email=bob@example.com&parent_email=charlie@example.com" \
    -H "Authorization: Bearer $TOKEN" \

# --------------------------------------------------------------------

materialid=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/create_material?course_id=$mathcourseid&title=Lecture%20material&description=Lecture%20material%20describtion" | extract_field material_id)

filematerialid=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -F "file=@./backend/tests/attachments.sh" \
    "$API_URL/create_material_attachment?course_id=$mathcourseid&material_id=$materialid" | extract_field file_id)

# --------------------------------------------------------------------

info=$(curl -s -X GET \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/get_material_attachments?course_id=$mathcourseid&material_id=$materialid")

expected='[
    {"course_id":"'"$mathcourseid"'","material_id":'$materialid',"file_id":"'"$filematerialid"'","filename":"attachments.sh"}
]'

json_partial_match_test "Request the list of material attachments from Alice" "$info" "$expected" "filename" "upload_time"

# --------------------------------------------------------------------

assignmentid=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/create_assignment?course_id=$mathcourseid&title=Assignment%201&description=To%20do%20exercise%2010%20from%20the%20course%20book" | extract_field assignment_id)

fileassignmentid=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -F "file=@./backend/tests/attachments.sh" \
    "$API_URL/create_assignment_attachment?course_id=$mathcourseid&assignment_id=$assignmentid" | extract_field file_id)

# --------------------------------------------------------------------

info=$(curl -s -X GET \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/get_assignment_attachments?course_id=$mathcourseid&assignment_id=$assignmentid")

expected='[
    {"course_id":"'"$mathcourseid"'","assignment_id":'$assignmentid',"file_id":"'"$fileassignmentid"'","filename":"attachments.sh"}
]'

json_partial_match_test "Request the list of assignment attachments from Alice" "$info" "$expected" "filename" "upload_time"

# --------------------------------------------------------------------

login_and_get_token "Login as Bob" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"bob@example.com\",\"password\":\"bobPass123!\"}"\

# --------------------------------------------------------------------

info=$(curl -s -X GET \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/get_material_attachments?course_id=$mathcourseid&material_id=$materialid")

expected='[
    {"course_id":"'"$mathcourseid"'","material_id":'$materialid',"file_id":"'"$filematerialid"'","filename":"attachments.sh"}
]'

json_partial_match_test "Request the list of material attachments from Bob" "$info" "$expected" "filename" "upload_time"

# --------------------------------------------------------------------

info=$(curl -s -X GET \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/get_assignment_attachments?course_id=$mathcourseid&assignment_id=$assignmentid")

expected='[
    {"course_id":"'"$mathcourseid"'","assignment_id":'$assignmentid',"file_id":"'"$fileassignmentid"'","filename":"attachments.sh"}
]'

json_partial_match_test "Request the list of assignment attachments from Bob" "$info" "$expected" "filename" "upload_time"

# --------------------------------------------------------------------

success_test "Submit assignment as Bob" \
    -X POST "$API_URL/submit_assignment?course_id=$mathcourseid&assignment_id=$assignmentid&comment=The%20answer%20is%2010" \
    -H "Authorization: Bearer $TOKEN" \

filesubmissionid=$(curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -F "file=@./backend/tests/attachments.sh" \
    "$API_URL/create_submission_attachment?course_id=$mathcourseid&assignment_id=$assignmentid" | extract_field file_id)

# --------------------------------------------------------------------

info=$(curl -s -X GET \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/get_submission_attachments?course_id=$mathcourseid&assignment_id=$assignmentid&student_email=bob@example.com")

expected='[
    {"course_id":"'"$mathcourseid"'","assignment_id":'$assignmentid',"file_id":"'"$filesubmissionid"'","filename":"attachments.sh"}
]'

json_partial_match_test "Request the list of submission attachments from Bob" "$info" "$expected" "filename" "upload_time"

# --------------------------------------------------------------------

login_and_get_token "Login as Charlie" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"charlie@example.com\",\"password\":\"charliePass123!\"}"\

# --------------------------------------------------------------------

info=$(curl -s -X GET \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/get_material_attachments?course_id=$mathcourseid&material_id=$materialid")

expected='[
    {"course_id":"'"$mathcourseid"'","material_id":'$materialid',"file_id":"'"$filematerialid"'","filename":"attachments.sh"}
]'

json_partial_match_test "Request the list of material attachments from Charlie" "$info" "$expected" "filename" "upload_time"

# --------------------------------------------------------------------

info=$(curl -s -X GET \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/get_assignment_attachments?course_id=$mathcourseid&assignment_id=$assignmentid")

expected='[
    {"course_id":"'"$mathcourseid"'","assignment_id":'$assignmentid',"file_id":"'"$fileassignmentid"'","filename":"attachments.sh"}
]'

json_partial_match_test "Request the list of assignment attachments from Charlie" "$info" "$expected" "filename" "upload_time"

# --------------------------------------------------------------------

info=$(curl -s -X GET \
    -H "Authorization: Bearer $TOKEN" \
    "$API_URL/get_submission_attachments?course_id=$mathcourseid&assignment_id=$assignmentid&student_email=bob@example.com")

expected='[
    {"course_id":"'"$mathcourseid"'","assignment_id":'$assignmentid',"file_id":"'"$filesubmissionid"'","filename":"attachments.sh"}
]'

json_partial_match_test "Request the list of submission attachments from Bob" "$info" "$expected" "filename" "upload_time"

# --------------------------------------------------------------------

login_and_get_token "Login as Admin" \
    -X POST $API_URL/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"admin\",\"password\":\"admin\"}"

success_test "Removing Alice account from Admin" \
    -X POST "$API_URL/remove_user?deleted_user_email=alice@example.com" \
    -H "Authorization: Bearer $TOKEN" \

success_test "Removing Bob account from Admin" \
    -X POST "$API_URL/remove_user?deleted_user_email=bob@example.com" \
    -H "Authorization: Bearer $TOKEN" \

success_test "Removing Charlie account from Admin" \
    -X POST "$API_URL/remove_user?deleted_user_email=charlie@example.com" \
    -H "Authorization: Bearer $TOKEN" \
