#!/usr/bin/env bash
set -euo pipefail

docker exec -i system_db psql -U postgres -d edhub -v ON_ERROR_STOP=1 -c "
  TRUNCATE TABLE
    users, 
    courses,
    course_section,
    course_materials,
    course_assignments,
    course_assignments_submissions,
    teaches,
    student_at,
    parent_of_at_course,
    logs,
    material_files,
    assignment_files,
    submissions_files
  RESTART IDENTITY CASCADE;
"

docker exec -i filestorage_db psql -U postgres -d edhub_storage -v ON_ERROR_STOP=1 -c "
  TRUNCATE TABLE
    files
  RESTART IDENTITY CASCADE;
"
