package schema

import (
	"time"

	"entgo.io/ent"
	"entgo.io/ent/schema/field"
)

// Backup holds the schema definition for the Backup entity.
type Backup struct {
	ent.Schema
}

// Fields of the Backup.
func (Backup) Fields() []ent.Field {
	return []ent.Field{
		field.Int("id").Positive(),
		field.String("device_ip").NotEmpty(),
		field.String("filename").NotEmpty(),
		field.Text("content").Default(""),
		field.Int64("size_bytes").Default(0),
		field.String("vendor").Default(""),
		field.Time("created_at").Default(time.Now).Immutable(),
	}
}
