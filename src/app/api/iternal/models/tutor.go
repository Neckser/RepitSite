package models

type AdminTutor struct {
	ID       string   `json:"id"`
	Name     string   `json:"name"`
	Subjects []string `json:"subjects"`
}
