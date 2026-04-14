package models

type AdminGrades struct {
	ID               string  `json:"id"`
	StudentID        string  `json:"student_id"`
	StudentFirstName string  `json:"student_first_name"`
	StudentLastName  string  `json:"student_fullname"`
	TutorId          string  `json:"tutor_id"`
	TutorFirstname   string  `json:"tutor_first_name"`
	TutorLastName    string  `json:"tutor_last_name"`
	Subject          string  `json:"subject"`
	Grade            int     `json:"grade"`
	Reason           *string `json:"reason"`
	Comment          *string `json:"comment"`
	Date             string  `json:"date"`
}
