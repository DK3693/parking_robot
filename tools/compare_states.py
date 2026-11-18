"""Offline comparison of NORMALIZED planar states. No ROS or robot commands.

Input is a JSON object with real/sim arrays, already transformed to the SAME
map/reference point and explicitly aligned to the SAME trial clock.
This module does not perform localization, clock calibration, or TF conversion.
"""
import argparse
import bisect
import json
import math
from pathlib import Path

IDENTITY = ('frame_id', 'map_revision', 'clock_id', 'epoch', 'robot_id',
            'reference_point', 'alignment_id')


def wrap(angle):
    return math.atan2(math.sin(angle), math.cos(angle))


def validate(states):
    if not states:
        raise ValueError('empty stream')
    previous = -math.inf
    first = states[0]
    for state in states:
        for key in IDENTITY:
            if not isinstance(state.get(key), str) or not state[key]:
                raise ValueError('missing identity: ' + key)
            if state[key] != first[key]:
                raise ValueError('identity changed: ' + key)
        for key in ('t_s', 'x_m', 'y_m', 'yaw_rad'):
            value = state.get(key)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError('invalid numeric field: ' + key)
        if state['t_s'] <= previous:
            raise ValueError('timestamps must strictly increase; split resets into new epochs')
        previous = state['t_s']


def interpolate(states, times, t, max_gap_s):
    index = bisect.bisect_left(times, t)
    if index < len(times) and times[index] == t:
        return states[index]
    if index == 0 or index == len(times):
        raise ValueError('no_bracket')
    a, b = states[index - 1], states[index]
    gap = b['t_s'] - a['t_s']
    if gap > max_gap_s:
        raise ValueError('sample_gap')
    w = (t - a['t_s']) / gap
    return dict(a, t_s=t, x_m=a['x_m'] + w * (b['x_m'] - a['x_m']),
                y_m=a['y_m'] + w * (b['y_m'] - a['y_m']),
                yaw_rad=wrap(a['yaw_rad'] + w * wrap(b['yaw_rad'] - a['yaw_rad'])))


def compare(real, sim, max_gap_s):
    if not math.isfinite(max_gap_s) or max_gap_s <= 0:
        raise ValueError('max_gap_s must be positive; this is a data-quality setting, not a safety limit')
    validate(real)
    validate(sim)
    for key in IDENTITY:
        if real[0][key] != sim[0][key]:
            raise ValueError('incompatible streams: ' + key)
    times = [s['t_s'] for s in sim]
    rows = []
    for r in real:
        try:
            s = interpolate(sim, times, r['t_s'], max_gap_s)
        except ValueError as error:
            rows.append({'t_s': r['t_s'], 'valid': False, 'reason': str(error)})
            continue
        dx, dy = r['x_m'] - s['x_m'], r['y_m'] - s['y_m']
        c, sn = math.cos(s['yaw_rad']), math.sin(s['yaw_rad'])
        rows.append({'t_s': r['t_s'], 'valid': True,
                     'longitudinal_m': c * dx + sn * dy,
                     'lateral_m': -sn * dx + c * dy,
                     'position_m': math.hypot(dx, dy),
                     'yaw_deg': math.degrees(wrap(r['yaw_rad'] - s['yaw_rad']))})
    valid = [r for r in rows if r['valid']]
    return {'meaning': 'difference between supplied estimates; NOT ground-truth accuracy',
            'comparison_frame': 'simulated robot heading at matching timestamp',
            'count_valid': len(valid), 'count_rejected': len(rows) - len(valid),
            'position_rmse_m': (math.sqrt(sum(r['position_m']**2 for r in valid) / len(valid))
                                if valid else None),
            'max_gap_s': max_gap_s, 'rows': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--max-gap-s', type=float, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text())
    print(json.dumps(compare(payload['real'], payload['sim'], args.max_gap_s), indent=2, allow_nan=False))
