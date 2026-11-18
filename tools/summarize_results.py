"""Recalculate the published alignment metrics from the complete selected series."""
import csv
import json
import math
from pathlib import Path
from statistics import mean

root = Path(__file__).resolve().parents[1]
with (root / 'data/alignment_trials.csv').open(newline='') as stream:
    rows = list(csv.DictReader(stream))
expected = json.loads((root / 'data/alignment_summary.json').read_text())
assert len(rows) == expected['sample_size']
assert len({row['trial_id'] for row in rows}) == len(rows)
assert sorted({float(row['initial_yaw_deg']) for row in rows}) == expected['configuration']['initial_angles_deg']
for angle in expected['configuration']['initial_angles_deg']:
    assert sum(float(row['initial_yaw_deg']) == angle for row in rows) == 2
success = sum(row['success'].lower() == 'true' for row in rows)
assert success == expected['successful_trials']
result = {'trials': len(rows), 'successful_trials': success}
for field, label in [('longitudinal_error_mm', 'longitudinal_mm'),
                     ('lateral_error_mm', 'lateral_mm'),
                     ('heading_error_deg', 'heading_deg')]:
    values = [abs(float(row[field])) for row in rows]
    assert all(math.isfinite(value) for value in values)
    result[label + '_mae'] = mean(values)
    result[label + '_max'] = max(values)
    assert math.isclose(mean(values), expected['mean_absolute_error'][label], rel_tol=1e-10)
result['mean_alignment_sim_s'] = mean(float(row['alignment_sim_s']) for row in rows)
assert math.isclose(result['mean_alignment_sim_s'], expected['mean_alignment_sim_s'], rel_tol=1e-10)
print(json.dumps(result, indent=2))
print('Published summary matches the CSV.')
