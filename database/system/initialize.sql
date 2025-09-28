CREATE DATABASE edhub;
\c edhub

-------------- MAIN TABLES --------------

CREATE TABLE users(
    email text PRIMARY KEY CHECK (length(email) <= 254),
    publicname text NOT NULL CHECK (length(publicname) <= 80),
    isadmin bool NOT NULL DEFAULT 'f',
    timeregistered timestamp NOT NULL,
    passwordhash text NOT NULL
);

CREATE TABLE courses(
    courseid uuid PRIMARY KEY,
    name text NOT NULL CHECK (length(name) BETWEEN 3 AND 80),
    organization text NULL CHECK (length(organization) BETWEEN 3 AND 80),
    instructor text NOT NULL REFERENCES users(email) ON DELETE CASCADE,
    timecreated timestamp NOT NULL
);

CREATE TABLE course_sections(
    courseid uuid REFERENCES courses ON DELETE CASCADE,
    sectionid serial NOT NULL,
    name text NOT NULL CHECK (length(name) BETWEEN 3 AND 80),
    sectionorder int NOT NULL CHECK (sectionorder >= 0),
    PRIMARY KEY (courseid, sectionid),
    CONSTRAINT course_sections_courseid_sectionorder_key
        UNIQUE (courseid, sectionorder)
        DEFERRABLE INITIALLY IMMEDIATE
);

CREATE TABLE course_materials(
    courseid uuid REFERENCES courses ON DELETE CASCADE,
    matid serial NOT NULL,
    timeadded timestamp NOT NULL,
    author text NULL REFERENCES users(email) ON DELETE SET NULL,
    name text NOT NULL CHECK (length(name) BETWEEN 3 AND 80),
    description text NOT NULL CHECK (length(description) BETWEEN 3 AND 10000),
    sectionid int NOT NULL,
    FOREIGN KEY (courseid, sectionid) REFERENCES course_sections(courseid, sectionid) ON DELETE CASCADE,
    PRIMARY KEY (courseid, matid)
);

CREATE TABLE course_assignments(
    courseid uuid REFERENCES courses ON DELETE CASCADE,
    assid serial NOT NULL,
    timeadded timestamp NOT NULL,
    author text NULL REFERENCES users(email) ON DELETE SET NULL,
    name text NOT NULL CHECK (length(name) BETWEEN 3 AND 80),
    description text NOT NULL CHECK (length(description) BETWEEN 3 AND 10000),
    sectionid int NOT NULL,
    FOREIGN KEY (courseid, sectionid) REFERENCES course_sections(courseid, sectionid) ON DELETE CASCADE,
    PRIMARY KEY (courseid, assid)
);

CREATE TABLE course_assignments_submissions(
    courseid uuid REFERENCES courses ON DELETE CASCADE,
    assid int NOT NULL,
    email text REFERENCES users ON DELETE CASCADE,
    timeadded timestamp NOT NULL,
    timemodified timestamp NOT NULL CHECK (timemodified >= timeadded),
    submissiontext text NOT NULL CHECK (length(submissiontext) BETWEEN 3 AND 10000),
    grade int NULL,
    comment text NULL CHECK (length(comment) BETWEEN 3 AND 10000),
    gradedby text NULL REFERENCES users ON DELETE SET NULL,
    FOREIGN KEY (courseid, assid) REFERENCES course_assignments ON DELETE CASCADE,
    PRIMARY KEY (courseid, assid, email)
);

CREATE TABLE teaches(
    email text REFERENCES users ON DELETE CASCADE,
    courseid uuid REFERENCES courses ON DELETE CASCADE,
    PRIMARY KEY (email, courseid)
);

CREATE TABLE student_at(
    email text REFERENCES users ON DELETE CASCADE,
    courseid uuid REFERENCES courses ON DELETE CASCADE,
    PRIMARY KEY (email, courseid)
);

CREATE TABLE parent_of_at_course(
    parentemail text REFERENCES users ON DELETE CASCADE,
    studentemail text REFERENCES users ON DELETE CASCADE,
    courseid uuid REFERENCES courses ON DELETE CASCADE,
    FOREIGN KEY (studentemail, courseid) REFERENCES student_at ON DELETE CASCADE,
    PRIMARY KEY (parentemail, studentemail, courseid)
);

CREATE TABLE logs(
    t timestamp NOT NULL,
    tag text NOT NULL,
    msg text NOT NULL
);

CREATE TABLE material_files(
    courseid uuid,
    matid int,
    fileid uuid,
    filename text NOT NULL CHECK (length(filename) <= 80),
    uploadtime timestamp NOT NULL,
    FOREIGN KEY (courseid, matid) REFERENCES course_materials ON DELETE CASCADE,
    PRIMARY KEY (courseid, matid, fileid)
);

CREATE TABLE assignment_files(
    courseid uuid,
    assid int,
    fileid uuid,
    filename text NOT NULL CHECK (length(filename) <= 80),
    uploadtime timestamp NOT NULL,
    FOREIGN KEY (courseid, assid) REFERENCES course_assignments ON DELETE CASCADE,
    PRIMARY KEY (courseid, assid, fileid)
);

CREATE TABLE submissions_files(
    courseid uuid,
    assid int,
    email text,
    fileid uuid,
    filename text NOT NULL CHECK (length(filename) <= 80),
    uploadtime timestamp NOT NULL,
    FOREIGN KEY (courseid, assid, email) REFERENCES course_assignments_submissions ON DELETE CASCADE,
    PRIMARY KEY (courseid, assid, email, fileid)
);

CREATE OR REPLACE FUNCTION create_default_section() RETURNS trigger AS $$
BEGIN
    INSERT INTO course_sections (courseid, name, sectionorder)
    VALUES (NEW.courseid, 'General', 0);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER courses_default_section_trigger
    AFTER INSERT ON courses
    FOR EACH ROW
    EXECUTE PROCEDURE create_default_section();

-------------- INDEXES --------------

CREATE INDEX idx_users_isadmin_true ON users(isadmin) WHERE isadmin = true;
CREATE INDEX idx_courses_instructor ON courses(instructor);
CREATE INDEX idx_materials_course_time ON course_materials(courseid, timeadded);
CREATE INDEX idx_assignments_course_time ON course_assignments(courseid, timeadded);
CREATE INDEX idx_submissions_course_ass_time ON course_assignments_submissions(courseid, assid, timeadded);
CREATE INDEX idx_material_files_fileid ON material_files(fileid);
CREATE INDEX idx_assignment_files_fileid ON assignment_files(fileid);
CREATE INDEX idx_submissions_files_fileid ON submissions_files(fileid);
CREATE INDEX idx_teaches_course ON teaches(courseid);
CREATE INDEX idx_student_at_course ON student_at(courseid);
CREATE INDEX idx_parent_course_student ON parent_of_at_course(courseid, studentemail);
CREATE INDEX idx_parent_course_parent ON parent_of_at_course(courseid, parentemail);
CREATE INDEX idx_logs_t ON logs(t);


-------------- PERSONAL COURSE INFO --------------

CREATE TABLE emoji(
    id serial PRIMARY KEY,
    name text NOT NULL CHECK (length(name) <= 80),
    fileid uuid
);

CREATE TABLE personal_course_info(
    courseid uuid REFERENCES courses ON DELETE CASCADE,
    email text REFERENCES users ON DELETE CASCADE,
    emojiid int NULL REFERENCES emoji(id) ON DELETE SET NULL,
    courseorder int NOT NULL CHECK (courseorder >= 0),
    PRIMARY KEY (courseid, email),
    CONSTRAINT personal_course_info_email_courseorder_key
        UNIQUE (email, courseorder)
        DEFERRABLE INITIALLY IMMEDIATE
);

CREATE OR REPLACE FUNCTION trg_personal_course_info()
RETURNS trigger AS $$
DECLARE
    v_email text;
    v_courseid uuid;
BEGIN
    CASE TG_TABLE_NAME
        WHEN 'student_at' THEN
            v_email := COALESCE(NEW.email, OLD.email);
            v_courseid := COALESCE(NEW.courseid, OLD.courseid);

        WHEN 'teaches' THEN
            v_email := COALESCE(NEW.email, OLD.email);
            v_courseid := COALESCE(NEW.courseid, OLD.courseid);

        WHEN 'parent_of_at_course' THEN
            v_email := COALESCE(NEW.parentemail, OLD.parentemail);
            v_courseid := COALESCE(NEW.courseid, OLD.courseid);

        WHEN 'courses' THEN
            v_email := COALESCE(NEW.instructor, OLD.instructor);
            v_courseid := COALESCE(NEW.courseid, OLD.courseid);
        ELSE
            RAISE EXCEPTION 'Unsupported table: %', TG_TABLE_NAME;
    END CASE;

    IF (TG_OP = 'INSERT') THEN
        INSERT INTO personal_course_info (courseid, email, courseorder)
        VALUES (
            v_courseid,
            v_email,
            COALESCE(
                (SELECT MAX(courseorder) + 1
                 FROM personal_course_info
                 WHERE email = v_email),
                0
            )
        )
        RETURN NEW;

    ELSIF (TG_OP = 'DELETE') THEN
        DELETE FROM personal_course_info
        WHERE courseid = v_courseid AND email = v_email;

        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_student_info
    AFTER INSERT OR DELETE ON student_at
    FOR EACH ROW EXECUTE FUNCTION trg_personal_course_info();

CREATE TRIGGER trg_teacher_info
    AFTER INSERT OR DELETE ON teaches
    FOR EACH ROW EXECUTE FUNCTION trg_personal_course_info();

CREATE TRIGGER trg_parent_info
    AFTER INSERT OR DELETE ON parent_of_at_course
    FOR EACH ROW EXECUTE FUNCTION trg_personal_course_info();

CREATE TRIGGER trg_instructor_info
    AFTER INSERT OR DELETE ON courses
    FOR EACH ROW EXECUTE FUNCTION trg_personal_course_info();
