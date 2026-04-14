package models

import (
	"fmt"
	"time"
)

type AdminHomeworks struct {
	ID               string         `json:"id"`
	StudentId        string         `json:"student_id"`
	StudentFirstName string         `json:"student_first_name"`
	StudentLastName  string         `json:"student_last_name"`
	TutorId          string         `json:"tutor_id"`
	TutorFirstName   string         `json:"tutor_first_name"`
	TutorLastName    string         `json:"tutor_lat_name"`
	Subject          string         `json:"subject"`
	Title            string         `json:"title"`
	Description      string         `json:"description"`
	Status           string         `json:"status"`
	Deadline         string         `json:"deadline"`
	CreatedAt        string         `json:"created_at"`
	Tasks            []HomeworkTask `json:"tasks"`
}

type HomeworkTask struct {
	ID         string `json:"task_id"`
	HomeworkId string `json:"homework_id"`
	Type       string `json:"type"`
	Content    string `json:"content"`
	Status     string `json:"status"`
}

type HomeworkCreateRequest struct {
	StudentID   string    `json:"student_id"`
	TutorID     string    `json:"tutor_id"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	Subject     string    `json:"subject"`
	Deadline    time.Time `json:"deadline"`
	Status      string    `json:"status"`
}

func (h *HomeworkCreateRequest) Validate() error {
	if h.StudentID == "" ||
		h.TutorID == "" ||
		h.Title == "" ||
		h.Subject == "" ||
		h.Status == "" {
		return fmt.Errorf("Обязательные поля пусты")
	}

	if h.Deadline.IsZero() {
		return fmt.Errorf("необходимо указать дедлайн")
	}
	return nil
}
