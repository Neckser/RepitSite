package service

import (
	"database/sql"
	"tutoring-api/iternal/models"

	"github.com/google/uuid"
	"golang.org/x/crypto/bcrypt"
)

type StudentService struct {
	db *sql.DB
}

func NewStudentService(db *sql.DB) *StudentService {
	return &StudentService{db: db}
}

func (s *StudentService) GetAllStudents() ([]models.AdminStudent, error) {
	var students []models.AdminStudent

	query := `SELECT student_id, first_name, last_name, grade, bio FROM students`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, err
	}

	defer rows.Close()

	for rows.Next() {
		var s models.AdminStudent

		err := rows.Scan(&s.ID, &s.FirstName, &s.LastName, &s.Grade, &s.Bio)
		if err != nil {
			return nil, err
		}

		students = append(students, s)
	}

	return students, nil
}

func (s *StudentService) CreateStudent(req models.StudentCreateRequest) (string, error) {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		return "", err
	}

	studentID := uuid.New().String()

	query := `INSERT INTO students (student_id, first_name, last_name, grade, login, password) VALUES ($1, $2, $3, $4, $5, $6)`

	_, err = s.db.Exec(query,
		studentID,
		req.FirstName,
		req.LastName,
		req.Grade,
		req.Login,
		string(hashedPassword),
	)

	if err != nil {
		return "", err
	}

	return studentID, nil
}
