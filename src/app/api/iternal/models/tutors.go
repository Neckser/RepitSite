package models

type AdminTutor struct {
	ID        string   `json:"id"`
	FirstName string   `json:"first_name"`
	LastName  string   `json:"last_name"`
	Subjects  []string `json:"subjects"`
}

type TutorCreateRequest struct {
	FirstName string   `json:"first_name"`
	LastName  string   `json:"last_name"`
	Login     string   `json:"login"`
	Password  string   `json:"password"`
	Subjects  []string `json:"subjects"`
}

func (r *TutorCreateRequest) Validate() error {
	if err := validateLogin(r.Login); err != nil {
		return err
	}
	if err := validatePassword(r.Password); err != nil {
		return err
	}
	return nil
}
