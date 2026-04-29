package models

import "time"

type AdminTutor struct {
	ID        string   `json:"id"`
	FirstName string   `json:"first_name"`
	LastName  string   `json:"last_name"`
	Subjects  []string `json:"subjects"`
}

// type TutorCreateRequest struct {
// 	FirstName string   `json:"first_name"`
// 	LastName  string   `json:"last_name"`
// 	Login     string   `json:"login"`
// 	Password  string   `json:"password"`
// 	Subjects  []string `json:"subjects"`
// }

type TutorCreateBadRequest struct {
	FirstName         string  `json:"first_name"`
	LastName          string  `json:"last_name"`
	Experience        int     `json:"experience"`
	Login             string  `json:"login"`
	Password          string  `json:"password"`
	SubjectMath       *string `json:"subject_math"`
	SubjectPhysics    *string `json:"subject_physics"`
	SubjectChemistry  *string `json:"subject_chemistry"`
	SubjectComputer   *string `json:"subject_computer"`
	SubjectRussian    *string `json:"subject_russian"`
	SubjectEnglish    *string `json:"subject_english"`
	SubjectGerman     *string `json:"subject_german"`
	SubjectFrench     *string `json:"subject_french"`
	SubjectHistory    *string `json:"subject_history"`
	SubjectSocial     *string `json:"subject_social"`
	SubjectLiterature *string `json:"subject_literature"`
	SubjectBiology    *string `json:"subject_biology"`
	SubjectGeography  *string `json:"subject_geography"`
	SubjectEconomics  *string `json:"subject_economics"`
	SubjectArt        *string `json:"subject_art"`
	SubjectMusic      *string `json:"subject_music"`
}

func (r *TutorCreateBadRequest) Validate() error {
	if err := validateLogin(r.Login); err != nil {
		return err
	}
	if err := validatePassword(r.Password); err != nil {
		return err
	}
	return nil
}

type AdminTutorInfo struct {
	ID               string    `json:"tutor_id"`
	FirstName        string    `json:"first_name"`
	LastName         string    `json:"last_name"`
	Bio              *string   `json:"bio"`
	Login            string    `json:"login"`
	Password         string    `json:"password"`
	RegistrationDate time.Time `json:"registration_date"`
}
