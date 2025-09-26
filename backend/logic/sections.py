from constants import TIME_FORMAT
import constraints
import repo.sections
import logic.logging as logger


def get_course_feed(db_cursor, course_id: str, user_email: str):
    constraints.assert_course_access(db_cursor, user_email, course_id)
    course_feed = repo.sections.sql_select_course_feed(db_cursor, course_id)
    res = [
        {
            "course_id": str(mat[0]),
            "post_id": mat[1],
            "section_id": mat[2],
            "section_name": mat[3],
            "section_order": mat[4],
            "type": mat[5],
            "timeadded": mat[6].strftime(TIME_FORMAT) if mat[6] is not None else None,
            "author": mat[7]
        }
        for mat in course_feed
    ]
    return res


def create_section(db_conn, db_cursor, course_id: str, title: str, user_email: str):
    # checking contraints
    constraints.assert_teacher_access(db_cursor, user_email, course_id)

    section_id = repo.sections.sql_insert_section(db_cursor, course_id, title)

    logger.log(db_conn, logger.TAG_SECTION_ADD, f"User {user_email} created a section {section_id} within the course {course_id}")
    return {"section_id": section_id}
