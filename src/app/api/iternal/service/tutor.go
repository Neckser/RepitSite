package service

import (
	"database/sql"
	"tutoring-api/iternal/models"

	"github.com/lib/pq"
)

type TutorService struct {
	db *sql.DB
}

func NewTutorService(db *sql.DB) *TutorService {
	return &TutorService{db: db}
}

func (s *TutorService) GetAllTutors() ([]models.AdminTutor, error) {
	var tutors []models.AdminTutor

	query := `
			SELECT 
			    tutor_id, 
			    first_name || ' ' || last_name AS name,
			    ARRAY_REMOVE(ARRAY[
			        CASE WHEN subject_math IS NOT NULL AND subject_math <> '' THEN 'Математика' END,
			        CASE WHEN subject_physics IS NOT NULL AND subject_physics <> '' THEN 'Физика' END,
			        CASE WHEN subject_chemistry IS NOT NULL AND subject_chemistry <> '' THEN 'Химия' END,
			        CASE WHEN subject_computer IS NOT NULL AND subject_computer <> '' THEN 'Информатика' END,
			        CASE WHEN subject_russian IS NOT NULL AND subject_russian <> '' THEN 'Русский язык' END,
			        CASE WHEN subject_english IS NOT NULL AND subject_english <> '' THEN 'Английский' END,
			        CASE WHEN subject_german IS NOT NULL AND subject_german <> '' THEN 'Немецкий' END,
			        CASE WHEN subject_french IS NOT NULL AND subject_french <> '' THEN 'Французский' END,
			        CASE WHEN subject_history IS NOT NULL AND subject_history <> '' THEN 'История' END,
			        CASE WHEN subject_social IS NOT NULL AND subject_social <> '' THEN 'Обществознание' END,
			        CASE WHEN subject_literature IS NOT NULL AND subject_literature <> '' THEN 'Литература' END,
			        CASE WHEN subject_biology IS NOT NULL AND subject_biology <> '' THEN 'Биология' END,
			        CASE WHEN subject_geography IS NOT NULL AND subject_geography <> '' THEN 'География' END,
			        CASE WHEN subject_economics IS NOT NULL AND subject_economics <> '' THEN 'Экономика' END,
			        CASE WHEN subject_art IS NOT NULL AND subject_art <> '' THEN 'ИЗО' END,
			        CASE WHEN subject_music IS NOT NULL AND subject_music <> '' THEN 'Музыка' END
			    ], NULL) AS subjects
			FROM tutors;`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var t models.AdminTutor
		err := rows.Scan(&t.ID, &t.Name, pq.Array(&t.Subjects))
		if err != nil {
			return nil, err
		}
		tutors = append(tutors, t)
	}

	return tutors, nil
}
