package auth

import (
	"golang.org/x/crypto/bcrypt"
)

const cost = bcrypt.DefaultCost

// HashPassword hashes a plain-text password with bcrypt.
func HashPassword(password string) (string, error) {
	b, err := bcrypt.GenerateFromPassword([]byte(password), cost)
	if err != nil {
		return "", err
	}
	return string(b), nil
}

// CheckPassword compares a bcrypt hash against a plain-text password.
func CheckPassword(hash, password string) bool {
	return bcrypt.CompareHashAndPassword([]byte(hash), []byte(password)) == nil
}
