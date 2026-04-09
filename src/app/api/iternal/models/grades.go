package models

type AdminGrades struct {
	ID              string  `json:"id"`
	StudentID       string  `json:"student_id"`
	StudentFullname string  `json:"student_fullname"`
	TutorId         string  `json:"tutor_id"`
	TutorFullname   string  `json:"tutor_fullname"`
	Subject         string  `json:"subject"`
	Grade           int     `json:"grade"`
	Reason          *string `json:"reason"`
	Comment         *string `json:"comment"`
	Date            string  `json:"date"`
}
