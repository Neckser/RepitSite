package service

import (
	"database/sql"
	"tutoring-api/iternal/models"
)

type HomeworksService struct {
	db *sql.DB
}

func NewHomeworksService(db *sql.DB) *HomeworksService {
	return &HomeworksService{db: db}
}

func (s *HomeworksService) GetAllHomeworks() ([]models.AdminHomeworks, error) {
	var homeworks []models.AdminHomeworks

	query := `SELECT h.homework_id, h.student_id, h.tutor_id, h.title, h.subject, h.description, h.status, h.deadline, h.created_at, s.first_name || ' ' || s.last_name AS student_fullname, t.first_name || ' ' || t.last_name AS tutor_fullname FROM homeworks h JOIN students s ON h.student_id = s.student_id JOIN tutors t ON h.tutor_id = t.tutor_id;`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var h models.AdminHomeworks
		if err := rows.Scan(&h.ID,
			&h.StudentId,
			&h.TutorId,
			&h.Title,
			&h.Subject,
			&h.Description,
			&h.Status,
			&h.Deadline,
			&h.CreatedAt,
			&h.StudentFullname,
			&h.TutorFullname); err != nil {
			return nil, err
		}
		homeworks = append(homeworks, h)
	}

	return homeworks, nil

}
