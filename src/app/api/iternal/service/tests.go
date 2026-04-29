package service

import (
	"database/sql"
	"encoding/json"
	"tutoring-api/iternal/models"
)

type TestService struct {
	db *sql.DB
}

func NewTestService(db *sql.DB) *TestService {
	return &TestService{db: db}
}

func (s *TestService) GetAllTests() ([]models.AdminTest, error) {
	testsMap := make(map[int]*models.AdminTest)
	var testIDs []int
	var result []models.AdminTest

	// 1. Получаем все "головы" тестов и данные участников
	query := `
        SELECT 
            t.test_id, t.tutor_id, t.student_id, t.title, t.subject, 
            t.date_start, t.date_end, t.created_at, t.duration,
            tut.first_name, tut.last_name,
            st.first_name, st.last_name
        FROM tests t
        JOIN tutors tut ON t.tutor_id = tut.tutor_id
        JOIN students st ON t.student_id = st.student_id
        ORDER BY t.created_at DESC;`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		t := new(models.AdminTest)
		t.Questions = make([]models.AdminQuestion, 0)

		err := rows.Scan(
			&t.TestID, &t.TutorID, &t.StudentID, &t.Title, &t.Subject,
			&t.DateStart, &t.DateEnd, &t.CreatedAt, &t.Duration,
			&t.TutorFirstName, &t.TutorLastName,
			&t.StudentFirstName, &t.StudentLastName,
		)
		if err != nil {
			return nil, err
		}

		testsMap[t.TestID] = t
		testIDs = append(testIDs, t.TestID)
	}

	if len(testIDs) == 0 {
		return []models.AdminTest{}, nil
	}

	// 2. Получаем ВСЕ вопросы для всех тестов одним махом
	questionRows, err := s.db.Query(`
        SELECT question_id, test_id, question_type, question_text, options 
        FROM test_questions 
        ORDER BY question_id ASC`)

	if err == nil {
		defer questionRows.Close()
		for questionRows.Next() {
			var q models.AdminQuestion
			var testID int
			var qOpt string

			err := questionRows.Scan(&q.QuestionID, &testID, &q.QuestionType, &q.QuestionText, &qOpt)
			if err == nil {
				// Распаковываем JSON-колонку options
				var rawOptions struct {
					Options       []string `json:"options"`
					Correct       any      `json:"correct"`
					CorrectAnswer any      `json:"correct_answer"` // Поддержка старой схемы
				}

				if errMarshal := json.Unmarshal([]byte(qOpt), &rawOptions); errMarshal == nil {
					// Наполняем нашу DTO данными
					q.Options = rawOptions.Options

					// Выбираем правильный ответ (любой из ключей)
					if rawOptions.Correct != nil {
						q.Correct = rawOptions.Correct
					} else {
						q.Correct = rawOptions.CorrectAnswer
					}

					// Если тест есть в нашей мапе, добавляем вопрос в слайс этого теста
					if targetTest, ok := testsMap[testID]; ok {
						targetTest.Questions = append(targetTest.Questions, q)
					}
				}
			}
		}
	}

	// 3. Собираем финальный результат, соблюдая порядок сортировки (от новых к старым)
	for _, id := range testIDs {
		result = append(result, *testsMap[id])
	}

	return result, nil
}
