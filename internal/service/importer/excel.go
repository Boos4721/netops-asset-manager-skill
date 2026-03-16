package importer

import (
	"fmt"
	"strings"

	"github.com/xuri/excelize/v2"
)

// DeviceRow represents a single device row from an import file.
type DeviceRow struct {
	IP       string
	Name     string
	Vendor   string
	Model    string
	Location string
	SN       string
	SSHUser  string
	SSHPass  string
	Tags     []string
}

// ParseExcel reads device rows from an xlsx file.
func ParseExcel(path string) ([]DeviceRow, error) {
	f, err := excelize.OpenFile(path)
	if err != nil {
		return nil, fmt.Errorf("open file: %w", err)
	}
	defer f.Close()

	sheets := f.GetSheetList()
	if len(sheets) == 0 {
		return nil, fmt.Errorf("no sheets found")
	}

	rows, err := f.GetRows(sheets[0])
	if err != nil {
		return nil, fmt.Errorf("get rows: %w", err)
	}

	if len(rows) < 2 {
		return nil, fmt.Errorf("file has no data rows")
	}

	// Build header index from first row
	header := rows[0]
	idx := make(map[string]int)
	for i, h := range header {
		idx[strings.ToLower(strings.TrimSpace(h))] = i
	}

	col := func(row []string, key string) string {
		i, ok := idx[key]
		if !ok || i >= len(row) {
			return ""
		}
		return strings.TrimSpace(row[i])
	}

	var devices []DeviceRow
	for _, row := range rows[1:] {
		ip := col(row, "ip")
		if ip == "" {
			ip = col(row, "管理ip") // Chinese header fallback
		}
		if ip == "" {
			continue
		}
		d := DeviceRow{
			IP:       ip,
			Name:     firstNonEmpty(col(row, "name"), col(row, "设备名")),
			Vendor:   firstNonEmpty(col(row, "vendor"), col(row, "品牌"), col(row, "厂商")),
			Model:    firstNonEmpty(col(row, "model"), col(row, "型号")),
			Location: firstNonEmpty(col(row, "location"), col(row, "位置"), col(row, "机房")),
			SN:       firstNonEmpty(col(row, "sn"), col(row, "序列号")),
			SSHUser:  firstNonEmpty(col(row, "ssh_user"), col(row, "user")),
			SSHPass:  firstNonEmpty(col(row, "ssh_pass"), col(row, "password")),
		}
		if tags := col(row, "tags"); tags != "" {
			for _, t := range strings.Split(tags, ",") {
				t = strings.TrimSpace(t)
				if t != "" {
					d.Tags = append(d.Tags, t)
				}
			}
		}
		devices = append(devices, d)
	}
	return devices, nil
}

func firstNonEmpty(vals ...string) string {
	for _, v := range vals {
		if v != "" {
			return v
		}
	}
	return ""
}
