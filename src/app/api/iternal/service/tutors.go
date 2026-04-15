package service

import (
	"database/sql"
	"tutoring-api/iternal/models"

	"github.com/google/uuid"
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
			    first_name,
				last_name,
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
		err := rows.Scan(&t.ID, &t.FirstName, &t.LastName, pq.Array(&t.Subjects))
		if err != nil {
			return nil, err
		}
		tutors = append(tutors, t)
	}

	return tutors, nil
}

// func (s *TutorService) CreateTutor(req models.TutorCreateRequest) (string, error) {
// 	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
// 	if err != nil {
// 		return "", err
// 	}

// 	tutorID := uuid.New().String()

// 	query := `INSERT INTO tutors (tutor_id, first_name, last_name, login, password, subjects) VALUES ($1, $2, $3, $4, $5, $6)`

// 	_, err = s.db.Exec(query,
// 		tutorID,
// 		req.FirstName,
// 		req.LastName,
// 		req.Login,
// 		string(hashedPassword),
// 		pq.Array(req.Subjects),
// 	)

// 	if err != nil {
// 		return "", err
// 	}

// 	return tutorID, nil
// }

func (s *TutorService) CreateTutor(req models.TutorCreateBadRequest) (string, error) {
	newUUID := uuid.New().String()

	query := `
        INSERT INTO tutors (
            tutor_id, first_name, last_name, 
            subject_math, subject_physics, subject_chemistry, 
            subject_computer, subject_russian, subject_english, 
            subject_german, subject_french, subject_history, 
            subject_social, subject_literature, subject_biology, 
            subject_geography, subject_economics, subject_art, 
            subject_music, experience, login, password
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, 
            $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22
        )
        RETURNING tutor_id`

	var returnedID string

	err := s.db.QueryRow(query,
		newUUID, req.FirstName, req.LastName,
		req.SubjectMath, req.SubjectPhysics, req.SubjectChemistry,
		req.SubjectComputer, req.SubjectRussian, req.SubjectEnglish,
		req.SubjectGerman, req.SubjectFrench, req.SubjectHistory,
		req.SubjectSocial, req.SubjectLiterature, req.SubjectBiology,
		req.SubjectGeography, req.SubjectEconomics, req.SubjectArt,
		req.SubjectMusic, req.Experience, req.Login, req.Password,
	).Scan(&returnedID)

	if err != nil {
		return "", err
	}

	return returnedID, nil
}

func (s *TutorService) LinkStudent(req models.AddRelationRequest) (bool, error) {
	query := `
        INSERT INTO student_tutors (student_id, tutor_id) 
        VALUES ($1, $2)
        ON CONFLICT (student_id, tutor_id) DO NOTHING
        RETURNING id`

	var lastID int
	err := s.db.QueryRow(query, req.StudentID, req.TutorID).Scan(&lastID)

	if err != nil {
		if err == sql.ErrNoRows {
			return false, nil
		}
		return false, err
	}

	return true, nil
}

func (s *TutorService) GetAllLinks() ([]models.AdminLinkResponse, error) {
	query := `
        SELECT 
            st.id, 
            st.student_id, s.first_name, s.last_name,
            st.tutor_id, t.first_name, t.last_name,
            st.start_date
        FROM student_tutors st
        JOIN students s ON st.student_id = s.student_id
        JOIN tutors t ON st.tutor_id = t.tutor_id
        ORDER BY st.start_date DESC`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var relations []models.AdminLinkResponse
	for rows.Next() {
		var r models.AdminLinkResponse
		err := rows.Scan(
			&r.ID,
			&r.StudentID, &r.StudentFirstName, &r.StudentLastName,
			&r.TutorID, &r.TutorFirstName, &r.TutorLastName,
			&r.StartDate,
		)
		if err != nil {
			return nil, err
		}
		relations = append(relations, r)
	}

	return relations, nil
}
