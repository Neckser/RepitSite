package models

import "fmt"

type AddRelationRequest struct {
	StudentID string `json:"student_id"`
	TutorID   string `json:"tutor_id"`
}

func (r *AddRelationRequest) Validate() error {
	if r.StudentID == "" || r.TutorID == "" {
		return fmt.Errorf("student_id и tutor_id обязательны")
	}
	return nil
}
