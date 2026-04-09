package models

type AdminHomeworks struct {
	ID              string `json:"id"`
	StudentId       string `json:"student_id"`
	StudentFullname string `json:"student_fullname"`
	TutorId         string `json:"tutor_id"`
	TutorFullname   string `json:"tutor_fullname"`
	Subject         string `json:"subject"`
	Title           string `json:"title"`
	Description     string `json:"description"`
	Status          string `json:"status"`
	Deadline        string `json:"deadline"`
	CreatedAt       string `json:"created_at"`
}
