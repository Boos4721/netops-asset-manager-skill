package handler

import (
	"io/fs"
	"net/http"

	"github.com/gin-gonic/gin"
)

// NewSPAHandler returns a handler that serves the embedded dist/ SPA,
// falling back to index.html for all non-file routes (client-side routing).
func NewSPAHandler(distFS fs.FS) gin.HandlerFunc {
	fileServer := http.FileServer(http.FS(distFS))
	return func(c *gin.Context) {
		path := c.Request.URL.Path
		// Try to open the file
		f, err := distFS.Open(path)
		if err != nil {
			// Not found - serve index.html for SPA routing
			index, err2 := distFS.Open("index.html")
			if err2 != nil {
				c.Status(http.StatusNotFound)
				return
			}
			index.Close()
			c.Request.URL.Path = "/index.html"
		} else {
			f.Close()
		}
		fileServer.ServeHTTP(c.Writer, c.Request)
	}
}
