package models

import "time"

type AdminTest struct {
	TestID           int             `json:"test_id"`
	TutorID          string          `json:"tutor_id"`
	StudentID        string          `json:"student_id"`
	Title            string          `json:"test_title"`
	Subject          string          `json:"subject"`
	DateStart        time.Time       `json:"date_start"`
	DateEnd          time.Time       `json:"date_end"`
	CreatedAt        time.Time       `json:"created_at"`
	Duration         int             `json:"test_duration"`
	TutorFirstName   string          `json:"tutor_first_name,omitempty"`
	TutorLastName    string          `json:"tutor_last_name,omitempty"`
	StudentFirstName string          `json:"student_first_name,omitempty"`
	StudentLastName  string          `json:"student_last_name,omitempty"`
	Questions        []AdminQuestion `json:"questions"`
}

type AdminQuestion struct {
	QuestionID   int      `json:"question_id"`
	QuestionType string   `json:"question_type"`
	QuestionText string   `json:"question_text"`
	Options      []string `json:"options,omitempty"`
	Correct      any      `json:"correct"`
}
