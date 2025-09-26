from typing import List, Tuple, Optional
from uuid import UUID
from datetime import datetime


def sql_select_course_feed(db_cursor, course_id: str) -> List[Tuple[UUID, int, int, str, int, str, datetime, Optional[str]]]:
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
