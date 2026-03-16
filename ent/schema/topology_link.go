package schema

import (
	"time"

	"entgo.io/ent"
	"entgo.io/ent/schema/field"
)

// TopologyLink holds the schema definition for the TopologyLink entity.
type TopologyLink struct {
	ent.Schema
}

// Fields of the TopologyLink.
func (TopologyLink) Fields() []ent.Field {
	return []ent.Field{
		field.Int("id").Positive(),
		field.String("source_ip").NotEmpty(),
		field.String("target_ip").NotEmpty(),
		field.String("link_type").Default("logical"),
		field.String("label").Default(""),
		field.Time("created_at").Default(time.Now).Immutable(),
	}
}
