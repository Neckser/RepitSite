package models

import "fmt"

type AddRelationRequest struct {
	StudentID string `json:"student_id"`
	TutorID   string `json:"tutor_id"`
}

type AdminLinkResponse struct {
	ID               int    `json:"id"`
	StudentID        string `json:"student_id"`
	StudentFirstName string `json:"student_first_name"`
	StudentLastName  string `json:"student_last_name"`
	TutorID          string `json:"tutor_id"`
	TutorFirstName   string `json:"tutor_first_name"`
	TutorLastName    string `json:"tutor_last_name"`
	StartDate        string `json:"start_date"`
}

func (r *AddRelationRequest) Validate() error {
	if r.StudentID == "" || r.TutorID == "" {
		return fmt.Errorf("student_id и tutor_id обязательны")
	}
	return nil
}
