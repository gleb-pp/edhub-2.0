from typing import List, Tuple, Optional
from uuid import UUID
from datetime import datetime

def sql_select_available_courses(db_cursor, user_email: str) -> List[UUID]:
    db_cursor.execute(
        """
        SELECT courseid FROM personal_course_info WHERE email = %s
        """,
        (user_email, ),
    )
    return [i[0] for i in db_cursor.fetchall()]


def sql_select_all_courses(db_cursor) -> List[UUID]:
    db_cursor.execute("SELECT courseid FROM courses")
    return [i[0] for i in db_cursor.fetchall()]


def sql_insert_course(db_cursor, title: str, instructor: str, organization: Optional[str] = None) -> UUID:
    db_cursor.execute(
        "INSERT INTO courses (courseid, name, organization, instructor, timecreated) VALUES (gen_random_uuid(), %s, %s, %s, now()) RETURNING courseid",
        (title, organization, instructor),
    )
    return db_cursor.fetchone()[0]


def sql_delete_course(db_cursor, course_id: str) -> None:
    db_cursor.execute("DELETE FROM courses WHERE courseid = %s", (course_id,))


def sql_select_course_info(db_cursor, course_id: str) -> Optional[Tuple[UUID, str, str, Optional[str], datetime]]:
    db_cursor.execute(
        """
        SELECT courseid, name, instructor, organization, timecreated
        FROM courses
        WHERE courseid = %s
        """,
        (course_id,),
    )
    return db_cursor.fetchone()


def sql_update_courses_order(db_cursor, new_order: List[str], user_email: str) -> None:

    # postpone the checking of uniqueness contraints
    db_cursor.execute("SET CONSTRAINTS personal_course_info_email_courseorder_key DEFERRED")

    # set correct values
    values_to_update = [(course_id, index) for index, course_id in enumerate(new_order)]
    values_str = ", ".join(f"(%s, %s)" for _ in values_to_update)
    flat_values = [val for pair in values_to_update for val in pair]
    db_cursor.execute(f"""
        UPDATE personal_course_info pci
        SET courseorder = new.courseorder
        FROM (VALUES {values_str}) AS new(courseid, courseorder)
        WHERE pci.email = %s AND pci.courseid = new.courseid::uuid
        """,
        flat_values + [user_email]
    )
