package service

import (
	"database/sql"
	"tutoring-api/iternal/models"
)

type StatsService struct {
	db *sql.DB
}

func NewStatsService(db *sql.DB) *StatsService {
	return &StatsService{db: db}
}

func (s *StatsService) GetGlobalStats() (models.AdminStats, error) {
	var stats models.AdminStats

	query := `SELECT (SELECT COUNT(*) FROM students),
					(SELECT COUNT(*) FROM tutors),
					(SELECT COUNT(*) FROM homeworks),
					(SELECT COUNT(*) FROM grades),
					(SELECT COUNT(*) FROM timetable)`

	err := s.db.QueryRow(query).Scan(
		&stats.TotalStudents,
		&stats.TotalTutors,
		&stats.TotalHomeworks,
		&stats.TotalGrades,
		&stats.TotalLessons,
	)

	return stats, err

}
