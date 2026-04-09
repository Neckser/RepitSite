package models

type AdminStats struct {
	TotalStudents  int `json:"total_students"`
	TotalTutors    int `json:"total_tutors"`
	TotalHomeworks int `json:"total_homeworks"`
	TotalGrades    int `json:"total_grades"`
	TotalLessons   int `json:"total_lessons"`
}
