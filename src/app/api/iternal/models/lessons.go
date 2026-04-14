package models

type AdminLesson struct {
	ID               string       `json:"id"`
	StudentID        string       `json:"student_id"`
	StudentFirstName string       `json:"student_first_name"`
	StudentLastName  string       `json:"student_last_name"`
	TutorId          string       `json:"tutor_id"`
	TutorFirstName   string       `json:"tutor_first_name"`
	TutorLastName    string       `json:"tutor_lat_name"`
	Subject          string       `json:"subject"`
	Date             string       `json:"date"`
	Time             string       `json:"time"`
	Duration         int          `json:"duration"`
	Status           string       `json:"status"`
	Notes            *string      `json:"notes"`
	Tasks            []LessonTask `json:"tasks"`
	Links            []LessonLink `json:"links"`
	Desks            []LessonDesk `json:"desks"`
}

type LessonTask struct {
	ID      string  `json:"id"`
	Type    *string `json:"type"`
	Content *string `json:"content"`
}

type LessonLink struct {
	ID   string  `json:"id"`
	Link *string `json:"link"`
}

type LessonDesk struct {
	ID   string  `json:"id"`
	Desk *string `json:"desk"`
}
