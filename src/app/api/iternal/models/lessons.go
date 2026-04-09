package models

type AdminLesson struct {
	ID              string  `json:"id"`
	StudentID       string  `json:"student_id"`
	StudentFullname string  `json:"student_fullname"`
	TutorId         string  `json:"tutor_id"`
	TutorFullname   string  `json:"tutor_fullname"`
	Subject         string  `json:"subject"`
	Date            string  `json:"date"`
	Time            string  `json:"time"`
	Duration        int     `json:"duration"`
	Status          string  `json:"status"`
	Notes           *string `json:"notes"`
}
