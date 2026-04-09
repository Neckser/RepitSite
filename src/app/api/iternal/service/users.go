package service

import (
	"database/sql"
	"tutoring-api/iternal/models"
)

type UserService struct {
	db *sql.DB
}

func NewUserService(db *sql.DB) *UserService {
	return &UserService{db: db}
}

func (s *UserService) GetAllUsers() ([]models.AdminUsers, error) {
	var users []models.AdminUsers

	query := `SELECT tutor_id as id, first_name || ' ' || last_name, 'Репетитор' as role FROM tutors
		UNION ALL
		SELECT student_id as id, first_name || ' ' || last_name, 'Студент' as role FROM students`

	rows, err := s.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var u models.AdminUsers
		if err := rows.Scan(&u.ID, &u.Name, &u.Role); err != nil {
			return nil, err
		}
		users = append(users, u)
	}

	return users, nil

}
