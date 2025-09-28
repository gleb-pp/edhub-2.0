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


def sql_select_course_info(db_cursor, course_id: str, user_email: str) -> Optional[Tuple[UUID, str, str, Optional[str], datetime, Optional[int]]]:
    db_cursor.execute(
        """
        SELECT c.courseid, c.name, c.instructor, c.organization, c.timecreated, psi.emojiid
        FROM courses c
        JOIN personal_course_info pci ON c.courseid = pci.courseid
        WHERE psi.courseid = %s AND pci.email = %s
        """,
        (course_id,),
    )
    return db_cursor.fetchone()
