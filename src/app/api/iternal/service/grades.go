package service

import (
	"database/sql"
	"tutoring-api/iternal/models"
)

type GradeService struct {
	db *sql.DB
}

func NewGradeService(db *sql.DB) *GradeService {
	return &GradeService{db: db}
}

func (s *GradeService) GetAllGrades() ([]models.AdminGrades, error) {
	var grades []models.AdminGrades

	query := `
		SELECT 
			g.grade_id::TEXT, 
			g.student_id, 
			s.first_name || ' ' || s.last_name, 
			g.tutor_id, 
			t.first_name || ' ' || t.last_name, 
			g.subject, 
			g.grade, 
			g.description, 
			g.tutor_comment, 
			g.date::TEXT
		FROM grades g
		JOIN students s ON g.student_id = s.student_id
		JOIN tutors t ON g.tutor_id = t.tutor_id
		ORDER BY g.date DESC;
	`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var g models.AdminGrades

		err := rows.Scan(
			&g.ID,
			&g.StudentID,
			&g.StudentFullname,
			&g.TutorId,
			&g.TutorFullname,
			&g.Subject,
			&g.Grade,
			&g.Reason,
			&g.Comment,
			&g.Date,
		)
		if err != nil {
			return nil, err
		}
		grades = append(grades, g)
	}

	return grades, nil
}
