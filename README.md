## What is EdHub?


We want to develop a Learning Management System for interaction between teachers, students, and parents. Teachers can create courses, upload materials, create homework assignments, see student submissions, grade them based on criteria, and calculate course grade.


Our goal is to develop a platform that both school teachers can use in their classes and university professors can use when planning courses. In our project, we want to emphasize the simplicity and usability of the product. We want any school teacher, who does not know much about technology, too be able to use our LMS and improve the quality of an educational process.

Most existing LMSs have limited functionality and cannot be fully utilized in schools and universities. For example, [Google Classroom](https://classroom.google.com/) has a user-friendly interface and pleasant design, but does not support parental access, creating the need for teachers to explain the details of grades to students' parents, does not support the grading of entire course as well as the tracking of student attendance. In addition, Google Classroom is a proprietary platform that hosted by Google and can not be launched on local servers.

On the other hand, a lot of LMSs have awkward website design and cause difficulties in everyday use. For example, [Moodle](https://moodle.org/) platform has extensive functionality, but is too complex to use, requiring clear customization and support at the IT administrator level. In addition, the platform has no assessment of assignments by criteria.

## 🚀 How to Launch

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

### Quick Start
```bash
# Clone repository
git clone https://github.com/IU-Capstone-Project-2025/edhub.git
cd edhub

# Build and start containers
docker-compose up --build

# To run in detached mode:
# docker-compose up --build -d
```

### Services Overview
| Service       | Access URL                     | Port  | Notes                     |
|---------------|--------------------------------|-------|---------------------------|
| **Backend**   | http://localhost:8000         | 8000  | FastAPI application       |
| **Database**  | postgresql://db:5432/edhub    | 5432  | PostgreSQL container      |

### API Endpoints
| Method | Endpoint           | Description                          |
|--------|--------------------|--------------------------------------|
| GET    | `/available_courses` | List accessible courses for user    |
| GET    | `/get_course_feed`   | Get course materials feed           |
| GET    | `/get_material`      | Get specific material details       |
| POST   | `/create_material`   | Create new course material          |
| POST   | `/create_course`     | Create new course                   |
| POST   | `/invite_student`    | Invite student to course            |
| POST   | `/invite_parent`     | Invite parent to follow student     |

### Maintenance Commands
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs -f

# Rebuild from scratch
docker-compose down -v && docker-compose up --build
```

## Configuration

### Environment Variables
| Variable            | Default Value                         | Description                |
|---------------------|---------------------------------------|----------------------------|
| POSTGRES_USER       | postgres                              | Database username          |
| POSTGRES_PASSWORD   | 12345678                              | Database password          |
| DATABASE_URL        | postgresql://postgres:12345678@db:5432/edhub | Connection string         |

---