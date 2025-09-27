from typing import List, Tuple, Optional
from uuid import UUID
from datetime import datetime


def sql_select_course_feed(db_cursor, course_id: str) -> List[Tuple[UUID, Optional[int], int, str, int, Optional[str], Optional[datetime], Optional[str]]]:
    db_cursor.execute(
        """
        SELECT cs.courseid, feed.postid, cs.sectionid, cs.name, cs.sectionorder, feed.type, feed.timeadded, feed.author
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


def sql_insert_section(db_cursor, course_id: str, title: str) -> int:
    db_cursor.execute(
        """
        INSERT INTO course_section (courseid, name, sectionorder)
        VALUES (%s, %s, 
            (SELECT COALESCE(MAX(sectionorder), -1) + 1 FROM course_section WHERE courseid = %s)
        )
        RETURNING sectionid
        """,
        (course_id, title, course_id),
    )
    return db_cursor.fetchone()[0]


def sql_select_sections(db_cursor, course_id: str) -> List[int]:
    db_cursor.execute(
        """
        SELECT sectionid FROM course_section WHERE courseid = %s
        """,
        (course_id, ),
    )
    return [i[0] for i in db_cursor.fetchall()]


def sql_update_section_order(db_cursor, course_id: str, new_order: List[int]) -> None:
    for final_order, section_id in enumerate(new_order):
        db_cursor.execute(
            """
            UPDATE course_section
            SET sectionorder = %s
            WHERE courseid = %s AND sectionid = %s
            """,
            (final_order, course_id, section_id)
        )
