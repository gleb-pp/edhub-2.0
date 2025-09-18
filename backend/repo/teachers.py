from typing import List, Tuple

def sql_select_course_teachers(db_cursor, course_id: str) -> List[Tuple[str, str]]:
    db_cursor.execute(
        """
        SELECT t.email, u.publicname
        FROM teaches t
        JOIN users u ON t.email = u.email
        WHERE t.courseid = %s
        """,
        (course_id,),
    )
    return db_cursor.fetchall()


def sql_insert_teacher(db_cursor, course_id: str, new_teacher_email: str) -> None:
    db_cursor.execute(
        "INSERT INTO teaches (email, courseid) VALUES (%s, %s)",
        (new_teacher_email, course_id),
    )


def sql_delete_teacher(db_cursor, course_id: str, removing_teacher_email: str) -> None:
    db_cursor.execute(
        "DELETE FROM teaches WHERE courseid = %s AND email = %s",
        (course_id, removing_teacher_email),
    )


def sql_update_instructor(db_cursor, course_id: str, new_instructor: str) -> None:
    db_cursor.execute(
        "UPDATE courses SET instructor = %s WHERE course_id = %s",
        (new_instructor, course_id),
    )
