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

	homeworksMap := make(map[string]*models.AdminHomeworks)
	var hwIDs []string
	var result []models.AdminHomeworks

	query := `
		SELECT 
			h.homework_id::TEXT, 
			h.student_id, 
			h.tutor_id, 
			h.title, 
			h.subject, 
			h.description, 
			h.status, 
			h.deadline::TEXT, 
			h.created_at::TEXT, 
			s.first_name,
			s.last_name, 
			t.first_name,
			t.last_name
		FROM homeworks h 
		JOIN students s ON h.student_id = s.student_id 
		JOIN tutors t ON h.tutor_id = t.tutor_id
		ORDER BY h.created_at DESC;`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var h models.AdminHomeworks
		h.Tasks = make([]models.HomeworkTask, 0)

		err := rows.Scan(
			&h.ID,
			&h.StudentId,
			&h.TutorId,
			&h.Title,
			&h.Subject,
			&h.Description,
			&h.Status,
			&h.Deadline,
			&h.CreatedAt,
			&h.StudentFirstName,
			&h.StudentLastName,
			&h.TutorFirstName,
			&h.TutorLastName,
		)
		if err != nil {
			return nil, err
		}

		homeworksMap[h.ID] = &h
		hwIDs = append(hwIDs, h.ID)
	}

	if len(hwIDs) == 0 {
		return []models.AdminHomeworks{}, nil
	}

	taskRows, err := s.db.Query(`
        SELECT 
            task_id::TEXT, 
            homework_id::TEXT, 
            type, 
            content, 
            status 
        FROM homework_tasks 
        ORDER BY homework_id, task_id::INTEGER ASC;`)

	if err != nil {
		return nil, err
	}
	defer taskRows.Close()

	for taskRows.Next() {
		var t models.HomeworkTask
		err := taskRows.Scan(
			&t.ID,
			&t.HomeworkId,
			&t.Type,
			&t.Content,
			&t.Status,
		)
		if err != nil {
			return nil, err
		}

		if hw, ok := homeworksMap[t.HomeworkId]; ok {
			hw.Tasks = append(hw.Tasks, t)
		}
	}

	for _, id := range hwIDs {
		result = append(result, *homeworksMap[id])
	}

	return result, nil
}

func (s *HomeworksService) CreateHomework(req models.HomeworkCreateRequest) (bool, error) {

	query := `INSERT INTO homeworks (student_id, tutor_id, title, description, subject, deadline) VALUES ($1, $2, $3, $4, $5, $6) RETURNING homework_id;`

	_, err := s.db.Exec(query,
		req.StudentID,
		req.TutorID,
		req.Title,
		req.Description,
		req.Subject,
		req.Deadline,
	)
	if err != nil {
		return false, err
	}

	return true, nil
}
