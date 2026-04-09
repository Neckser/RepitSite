package models

type AdminUsers struct {
	ID       string `json:"id"`
	FullName string `json:"fullname"`
	Role     string `json:"role"`
}
