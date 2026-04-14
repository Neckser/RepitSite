package models

import (
	"fmt"
	"regexp"
	"unicode"
)

func validateLogin(login string) error {
	if len(login) < 6 {
		return fmt.Errorf("Логин должен содержать не менее 6 символов")
	}

	match, _ := regexp.MatchString("^[a-zA-Z0-9]+$", login)
	if !match {
		return fmt.Errorf("Логин должен содержать только латинские буквы и цифры")
	}
	return nil
}

func validatePassword(password string) error {
	if len(password) < 8 {
		return fmt.Errorf("Пароль должен содержать не менее 8 символов")
	}

	var (
		hasUpper bool
		hasLower bool
		hasDigit bool
	)

	for _, char := range password {
		switch {
		case unicode.IsUpper(char):
			hasUpper = true
		case unicode.IsLower(char):
			hasLower = true
		case unicode.IsDigit(char):
			hasDigit = true
		}
	}

	if !hasUpper {
		return fmt.Errorf("Пароль должен содержать хотя бы одну заглавную букву")
	}
	if !hasLower {
		return fmt.Errorf("Пароль должен содержать хотя бы одну строчную букву")
	}
	if !hasDigit {
		return fmt.Errorf("Пароль должен содержать хотя бы одну цифру")
	}
	return nil
}
