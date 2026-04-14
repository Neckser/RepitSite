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
	lessonsMap := make(map[string]*models.AdminLesson)
	var lessonIDs []string
	var result []models.AdminLesson

	query := `
        SELECT 
            t.schedule_id::TEXT, t.student_id, s.first_name, s.last_name, 
            t.tutor_id, tut.first_name, tut.last_name, t.subject, 
            t.lesson_date::TEXT, t.lesson_time::TEXT, t.duration, t.status, t.notes
        FROM timetable t
        JOIN students s ON t.student_id = s.student_id
        JOIN tutors tut ON t.tutor_id = tut.tutor_id
        ORDER BY t.lesson_date DESC, t.lesson_time DESC;`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		l := new(models.AdminLesson)
		l.Tasks = make([]models.LessonTask, 0)
		l.Links = make([]models.LessonLink, 0)
		l.Desks = make([]models.LessonDesk, 0)

		if err := rows.Scan(
			&l.ID, &l.StudentID, &l.StudentFirstName, &l.StudentLastName,
			&l.TutorId, &l.TutorFirstName, &l.TutorLastName, &l.Subject,
			&l.Date, &l.Time, &l.Duration, &l.Status, &l.Notes,
		); err != nil {
			return nil, err
		}
		lessonsMap[l.ID] = l
		lessonIDs = append(lessonIDs, l.ID)
	}

	if len(lessonIDs) == 0 {
		return []models.AdminLesson{}, nil
	}

	taskRows, err := s.db.Query(`SELECT task_id::TEXT, schedule_id::TEXT, type, content FROM lesson_tasks ORDER BY created_at ASC`)
	if err == nil {
		defer taskRows.Close()
		for taskRows.Next() {
			var t models.LessonTask
			var scheduleID string
			if err := taskRows.Scan(&t.ID, &scheduleID, &t.Type, &t.Content); err == nil {
				if l, ok := lessonsMap[scheduleID]; ok {
					l.Tasks = append(l.Tasks, t)
				}
			}
		}
	}

	linkRows, err := s.db.Query(`SELECT link_id::TEXT, schedule_id::TEXT, link FROM lesson_links ORDER BY created_at ASC`)
	if err == nil {
		defer linkRows.Close()
		for linkRows.Next() {
			var ln models.LessonLink
			var scheduleID string
			if err := linkRows.Scan(&ln.ID, &scheduleID, &ln.Link); err == nil {
				if l, ok := lessonsMap[scheduleID]; ok {
					l.Links = append(l.Links, ln)
				}
			}
		}
	}

	deskRows, err := s.db.Query(`SELECT desk_id::TEXT, schedule_id::TEXT, desk FROM lesson_desks ORDER BY created_at ASC`)
	if err == nil {
		defer deskRows.Close()
		for deskRows.Next() {
			var d models.LessonDesk
			var scheduleID string
			if err := deskRows.Scan(&d.ID, &scheduleID, &d.Desk); err == nil {
				if l, ok := lessonsMap[scheduleID]; ok {
					l.Desks = append(l.Desks, d)
				}
			}
		}
	}

	for _, id := range lessonIDs {
		result = append(result, *lessonsMap[id])
	}

	return result, nil
}
