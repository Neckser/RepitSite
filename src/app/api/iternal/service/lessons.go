package service

import (
	"database/sql"
	"tutoring-api/iternal/models"
)

type LessonsService struct {
	db *sql.DB
}

func NewLessonService(db *sql.DB) *LessonsService {
	return &LessonsService{db: db}
}

func (s *LessonsService) GetAllLessons() ([]models.AdminLesson, error) {
	var lessons []models.AdminLesson

	query := `
		SELECT 
			t.schedule_id::TEXT, 
			t.student_id, 
			s.first_name || ' ' || s.last_name, 
			t.tutor_id, 
			tut.first_name || ' ' || tut.last_name, 
			t.subject, 
			t.lesson_date::TEXT, 
			t.lesson_time::TEXT, 
			t.duration, 
			t.status, 
			t.notes
		FROM timetable t
		JOIN students s ON t.student_id = s.student_id
		JOIN tutors tut ON t.tutor_id = tut.tutor_id
		ORDER BY t.lesson_date DESC, t.lesson_time DESC;
	`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	for rows.Next() {
		var l models.AdminLesson

		err := rows.Scan(
			&l.ID,
			&l.StudentID,
			&l.StudentFullname,
			&l.TutorId,
			&l.TutorFullname,
			&l.Subject,
			&l.Date,
			&l.Time,
			&l.Duration,
			&l.Status,
			&l.Notes,
		)
		if err != nil {
			return nil, err
		}
		lessons = append(lessons, l)
	}

	return lessons, nil

}
