package models

import "time"

type AdminChats struct {
	ID               string     `json:"chat_id"`
	StudentID        string     `json:"student_id"`
	StudentFirstname string     `json:"student_first_name"`
	StudentLastName  string     `json:"student_last_name"`
	TutorID          string     `json:"tutor_id"`
	TutorFirstName   string     `json:"tutor_first_name"`
	TutorLastName    string     `json:"tutor_last_name"`
	LastMessageText  *string    `json:"last_message_text"`
	LastMessageAt    *time.Time `json:"last_message_at"`
	CreatedAt        time.Time  `json:"created_at"`
}

type AdminMessages struct {
	ID          string    `json:"message_id"`
	ChatID      string    `json:"chat_id"`
	SenderID    string    `json:"sender_id"`
	SenderType  string    `json:"sender_type"`
	MessageText string    `json:"message_text"`
	CreatedAt   time.Time `json:"created_at"`
}
