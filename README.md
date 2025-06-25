## What is EdHub?

EdHub is a Learning Management System for interaction between teachers, students, and parents. It aims to improve the quality of an educational process, simplify the interaction between stakeholders, and improve student engagement in learning.

Any user can create a course becoming a **Teacher**, invite students and their parents, upload materials, create assignments, see student submissions, grade them based on criteria, and calculate course grade. You can also join the course as a **Student** to see the study materials and submit your homework or as a **Parent** to track the academic performance of your child.

Most existing LMSs either have limited functionality or have awkward website design and cause difficulties in everyday use. EdHub combines a self-contained and clear design, supporting all the necessary features but not bogging the user down with complex customizations.

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
docker compose up --build

# To run in detached mode:
# docker compose up --build -d
```
Now you can go to http://localhost/ to access the application.

### Services Overview
| Service       | Port  | Notes                  |
|---------------|-------|------------------------|
| **Frontend**  | 3000  | React application      |
| **Backend**   | 8000  | FastAPI application    |
| **Database**  | 5432  | PostgreSQL container   |
| **Nginx**     | 80    | Nginx reverse proxy    |

### API Endpoints

You can access the web version of API documentation at http://localhost/api/docs/.

### Maintenance Commands
```bash
# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# View logs
docker compose logs -f

# Rebuild from scratch
docker compose down -v && docker compose up --build
```