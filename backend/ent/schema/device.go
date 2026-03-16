package schema

import (
	"time"

	"entgo.io/ent"
	"entgo.io/ent/schema/field"
)

// Device holds the schema definition for the Device entity.
type Device struct {
	ent.Schema
}

// Fields of the Device.
func (Device) Fields() []ent.Field {
	return []ent.Field{
		field.Int("id").Positive(),
		field.String("ip").Unique().NotEmpty(),
		field.String("name").Default(""),
		field.String("vendor").Default(""),
		field.String("model").Default(""),
		field.String("location").Default(""),
		field.String("sn").Default(""),
		field.String("server").Default(""),
		field.String("driver").Default(""),
		field.JSON("tags", []string{}).Default([]string{}),
		field.String("ssh_user").Default("root"),
		field.String("ssh_pass").Default("").Sensitive(),
		field.Enum("status").Values("online", "offline", "unknown").Default("unknown"),
		field.Time("last_seen").Optional().Nillable(),
		field.Bool("gpu").Default(false),
		field.Time("created_at").Default(time.Now).Immutable(),
		field.Time("updated_at").Default(time.Now).UpdateDefault(time.Now),
	}
}
