from typing import List, Tuple, Optional
from uuid import UUID
from datetime import datetime

def sql_select_available_courses(db_cursor, user_email: str) -> List[UUID]:
    db_cursor.execute(
        """
        SELECT courseid AS cid FROM courses WHERE instructor = %s
        UNION
        SELECT courseid AS cid FROM teaches WHERE email = %s
        UNION
        SELECT courseid AS cid FROM student_at WHERE email = %s
        UNION
        SELECT courseid AS cid FROM parent_of_at_course WHERE parentemail = %s
        """,
        (user_email, user_email, user_email, user_email),
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


def sql_select_course_feed(db_cursor, course_id: str) -> List[Tuple[UUID, int, int, str, int, str, datetime, Optional[str]]]:
    db_cursor.execute(
        """
        SELECT cs.cid, feed.postid, cs.sectionid, cs.name, cs.sectionorder, feed.type, feed.timeadded, feed.author
        FROM 
            (SELECT courseid AS cid, matid as postid, sectionid, 'mat' as type, timeadded, author
            FROM course_materials
            WHERE courseid = %s
            UNION
            SELECT courseid AS cid, assid as postid, sectionid, 'ass' as type, timeadded, author
            FROM course_assignments
            WHERE courseid = %s) feed
            RIGHT JOIN 
                (SELECT courseid, sectionid, name, sectionorder
                FROM course_section
                WHERE courseid = %s) cs ON feed.sectionid = cs.sectionid
        ORDER BY cs.sectionorder ASC, feed.timeadded ASC
        """,
        (course_id, course_id, course_id),
    )
    return db_cursor.fetchall()


def sql_insert_section(db_cursor, course_id: str, title: str) -> None:
    db_cursor.execute(
        """
        INSERT INTO course_section (courseid, name, sectionorder)
        VALUES (%s, %s, 
            (SELECT COALESCE(MAX(sectionorder), -1) + 1 FROM course_section WHERE courseid = %s) + 1
        )
        RETURNING sectionid
        """,
        (course_id, title, course_id),
    )
    return db_cursor.fetchone()[0]
