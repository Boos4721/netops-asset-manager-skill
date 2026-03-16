package auth

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

const claimsKey = "claims"

// JWTAuth returns a Gin middleware that validates Bearer JWT tokens.
func JWTAuth(secret string) gin.HandlerFunc {
	return func(c *gin.Context) {
		header := c.GetHeader("Authorization")
		if !strings.HasPrefix(header, "Bearer ") {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing or invalid authorization header"})
			return
		}
		tokenStr := strings.TrimPrefix(header, "Bearer ")
		claims, err := ParseToken(secret, tokenStr)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid token: " + err.Error()})
			return
		}
		c.Set(claimsKey, claims)
		c.Next()
	}
}

// RoleRequired returns a middleware that enforces minimum role level.
// Roles hierarchy: root > operator > viewer
func RoleRequired(minRole string) gin.HandlerFunc {
	roleLevel := map[string]int{"viewer": 1, "operator": 2, "root": 3}
	return func(c *gin.Context) {
		claims, ok := c.Get(claimsKey)
		if !ok {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
			return
		}
		cl := claims.(*Claims)
		if roleLevel[cl.Role] < roleLevel[minRole] {
			c.AbortWithStatusJSON(http.StatusForbidden, gin.H{"error": "insufficient permissions"})
			return
		}
		c.Next()
	}
}

// GetClaims extracts Claims from the Gin context (set by JWTAuth).
func GetClaims(c *gin.Context) *Claims {
	v, _ := c.Get(claimsKey)
	if v == nil {
		return nil
	}
	return v.(*Claims)
}
