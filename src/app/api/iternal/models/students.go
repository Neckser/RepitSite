package models

import (
	"fmt"
	"time"
)

type AdminStudent struct {
	ID        string  `json:"student_id"`
	FirstName string  `json:"first_name"`
	LastName  string  `json:"last_name"`
	Grade     int     `json:"grade"`
	Bio       *string `json:"bio"`
}

type StudentCreateRequest struct {
	FirstName string `json:"first_name"`
	LastName  string `json:"last_name"`
	Grade     int    `json:"grade"`
	Login     string `json:"login"`
	Password  string `json:"password"`
}

type AdminStudentInfo struct {
	ID               string    `json:"student_id"`
	FirstName        string    `json:"first_name"`
	LastName         string    `json:"last_name"`
	Grade            int       `json:"grade"`
	Bio              *string   `json:"bio"`
	Login            string    `json:"login"`
	Password         string    `json:"password"`
	RegistrationDate time.Time `json:"registration_date"`
}

func (r *StudentCreateRequest) Validate() error {
	if r.Grade < 1 || r.Grade > 11 {
		return fmt.Errorf("Класс должен быть от 1 до 11")
	}

	if err := validateLogin(r.Login); err != nil {
		return err
	}

	if err := validatePassword(r.Password); err != nil {
		return err
	}

	return nil
}
