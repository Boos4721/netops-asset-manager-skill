package embedded

import (
	"embed"
	"io/fs"
)

//go:embed dist
var distFS embed.FS

// DistFS returns a sub-filesystem rooted at dist/.
// Returns nil if the dist/ directory is empty (dev mode).
func DistFS() fs.FS {
	sub, err := fs.Sub(distFS, "dist")
	if err != nil {
		return nil
	}
	return sub
}
