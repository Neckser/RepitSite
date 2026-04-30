package service

import (
	"database/sql"
	"tutoring-api/iternal/models"
)

type ChatService struct {
	db *sql.DB
}

func NewChatService(db *sql.DB) *ChatService {
	return &ChatService{db: db}
}

func (s *ChatService) GetAllChats() ([]models.AdminChats, error) {
	var chats []models.AdminChats

	query := `SELECT chats.chat_id, chats.student_id, students.first_name, students.last_name, chats.tutor_id, tutors.first_name, tutors.last_name, chats.last_message_text, chats.last_message_at, chats.created_at FROM chats INNER JOIN students ON chats.student_id = students.student_id INNER JOIN tutors ON chats.tutor_id = tutors.tutor_id;`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var chat models.AdminChats

		err := rows.Scan(
			&chat.ID,
			&chat.StudentID,
			&chat.StudentFirstname,
			&chat.StudentLastName,
			&chat.TutorID,
			&chat.TutorFirstName,
			&chat.TutorLastName,
			&chat.LastMessageText,
			&chat.LastMessageAt,
			&chat.CreatedAt,
		)

		if err != nil {
			return nil, err
		}

		chats = append(chats, chat)
	}

	return chats, nil
}

func (s *ChatService) GetMessagesByChatID(chat_id string) ([]models.AdminMessages, error) {
	var messages []models.AdminMessages

	query := `SELECT message_id, chat_id, sender_id, sender_type, message_text, created_at FROM messages WHERE chat_id = $1`

	rows, err := s.db.Query(query, chat_id)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var m models.AdminMessages

		err := rows.Scan(
			&m.ID,
			&m.ChatID,
			&m.SenderID,
			&m.SenderType,
			&m.MessageText,
			&m.CreatedAt,
		)
		if err != nil {
			return nil, err
		}

		messages = append(messages, m)
	}
	return messages, nil
}

func (s *ChatService) GetMessagesBySenderID(sender_id string) ([]models.AdminMessages, error) {
	var messages []models.AdminMessages

	query := `SELECT message_id, chat_id, sender_id, sender_type, message_text, created_at FROM messages WHERE sender_id = $1`

	rows, err := s.db.Query(query, sender_id)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var m models.AdminMessages

		err := rows.Scan(
			&m.ID,
			&m.ChatID,
			&m.SenderID,
			&m.SenderType,
			&m.MessageText,
			&m.CreatedAt,
		)
		if err != nil {
			return nil, err
		}

		messages = append(messages, m)
	}
	return messages, nil
}

func (s *ChatService) GetMessagesByChatAndSender(chat_id, sender_id string) ([]models.AdminMessages, error) {
	var messages []models.AdminMessages

	query := `SELECT message_id, chat_id, sender_id, sender_type, message_text, created_at FROM messages WHERE sender_id = $1 AND chat_id = $2;`

	rows, err := s.db.Query(query, sender_id, chat_id)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var m models.AdminMessages

		err := rows.Scan(
			&m.ID,
			&m.ChatID,
			&m.SenderID,
			&m.SenderType,
			&m.MessageText,
			&m.CreatedAt,
		)
		if err != nil {
			return nil, err
		}

		messages = append(messages, m)
	}
	return messages, nil
}
