import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import math
import unittest
from compare_states import compare


def state(t=0, **changes):
    value = dict(t_s=t, x_m=0., y_m=0., yaw_rad=0., frame_id='facility_map',
                 map_revision='demo-v1', clock_id='aligned-trial', epoch='trial-001',
                 robot_id='carrier-01', reference_point='front_base', alignment_id='synthetic-fixture')
    value.update(changes)
    return value


class Tests(unittest.TestCase):
    def test_identical(self):
        self.assertEqual(compare([state()], [state()], .2)['position_rmse_m'], 0)

    def test_known_displacement(self):
        r = compare([state(x_m=.03, y_m=.04)], [state()], .2)['rows'][0]
        self.assertAlmostEqual(r['position_m'], .05)
        self.assertAlmostEqual(r['longitudinal_m'], .03)

    def test_body_frame(self):
        r = compare([state(y_m=.1, yaw_rad=math.pi/2)], [state(yaw_rad=math.pi/2)], .2)['rows'][0]
        self.assertAlmostEqual(r['longitudinal_m'], .1)
        self.assertAlmostEqual(r['lateral_m'], 0)

    def test_interpolation(self):
        r = compare([state(.1, x_m=.1)], [state(), state(.2, x_m=.2)], .2)
        self.assertAlmostEqual(r['position_rmse_m'], 0)

    def test_wrapped_interpolation(self):
        r = compare([state(.1, yaw_rad=math.pi)],
                    [state(yaw_rad=math.radians(179)), state(.2, yaw_rad=math.radians(-179))], .2)
        self.assertAlmostEqual(r['rows'][0]['yaw_deg'], 0)

    def test_mismatch_rejected(self):
        for key in ('frame_id', 'clock_id', 'map_revision', 'epoch', 'robot_id', 'reference_point', 'alignment_id'):
            with self.subTest(key=key), self.assertRaises(ValueError):
                compare([state()], [state(**{key: 'different'})], .2)

    def test_no_extrapolation(self):
        r = compare([state(.3)], [state(), state(.2)], .2)
        self.assertEqual(r['rows'][0]['reason'], 'no_bracket')
        self.assertIsNone(r['position_rmse_m'])

    def test_missing_data(self):
        r = compare([state(.1)], [state(), state(1)], .2)
        self.assertEqual(r['rows'][0]['reason'], 'sample_gap')

    def test_clock_reset(self):
        with self.assertRaises(ValueError):
            compare([state(), state()], [state()], .2)

    def test_bad_numeric(self):
        with self.assertRaises(ValueError):
            compare([state(x_m=float('nan'))], [state()], .2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
