#!/usr/bin/env bash
set -euo pipefail

docker exec -i system_db psql -U postgres -d edhub -v ON_ERROR_STOP=1 -c "
  TRUNCATE TABLE
    submissions_files,
    assignment_files,
    material_files,
    course_assignments_submissions,
    course_assignments,
    course_materials,
    parent_of_at_course,
    student_at,
    teaches,
    logs,
    courses,
    users
  RESTART IDENTITY CASCADE;
"

docker exec -i filestorage_db psql -U postgres -d edhub_storage -v ON_ERROR_STOP=1 -c "
  TRUNCATE TABLE
    files
  RESTART IDENTITY CASCADE;
"
