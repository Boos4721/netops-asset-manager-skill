package handler

import (
	"io/fs"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

// NewSPAHandler returns a handler that serves the embedded dist/ SPA,
// falling back to index.html for all non-file routes (client-side routing).
func NewSPAHandler(distFS fs.FS) gin.HandlerFunc {
	fileServer := http.FileServer(http.FS(distFS))
	return func(c *gin.Context) {
		path := c.Request.URL.Path
		cleanPath := strings.TrimPrefix(path, "/")
		if cleanPath == "" {
			cleanPath = "."
		}

		// Try to open the file
		f, err := distFS.Open(cleanPath)
		if err != nil {
			// Not found - serve index.html for SPA routing
			c.Request.URL.Path = "/"
		} else {
			stat, statErr := f.Stat()
			f.Close()
			// If it's a directory and not the root, fallback to SPA to prevent directory listing or 301s
			if statErr == nil && stat.IsDir() && path != "/" {
				c.Request.URL.Path = "/"
			}
		}
		fileServer.ServeHTTP(c.Writer, c.Request)
	}
}
