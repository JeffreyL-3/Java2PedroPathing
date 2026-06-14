import json
import tempfile
import unittest
from pathlib import Path

import pathing_tool


ROOT = Path(__file__).resolve().parents[1]


class GeneratedArtifactTests(unittest.TestCase):
    def assert_artifact_matches(self, source: str, artifact: str) -> None:
        code = pathing_tool.strip_comments((ROOT / source).read_text())
        poses = pathing_tool.parse_pose_constants(code)
        runtime_poses = pathing_tool.resolve_runtime_pose_map(
            poses,
            alliance="blue",
            location="far",
            force_close_score1=False,
            start_close_skip_far=False,
        )
        path_defs = pathing_tool.parse_paths(code)
        follow_order, waits = pathing_tool.parse_follow_and_wait_sequence(code)
        actual = pathing_tool.build_output(runtime_poses, path_defs, follow_order, waits)
        expected = json.loads((ROOT / artifact).read_text())

        self.assertEqual(expected, actual)

    def test_example_artifact(self) -> None:
        self.assert_artifact_matches(
            "examples/ANewWorkingAuto.java",
            "blue_far_pathing.json",
        )

    def test_provided_sample_artifact(self) -> None:
        self.assert_artifact_matches(
            "samples/provided_working_code.java",
            "samples/provided_blue_far.json",
        )

    def test_updated_sample_artifact(self) -> None:
        self.assert_artifact_matches(
            "samples/updated_auto.java",
            "samples/updated_blue_far.json",
        )


class OutputFileTests(unittest.TestCase):
    def test_output_is_valid_json(self) -> None:
        source = ROOT / "examples" / "ANewWorkingAuto.java"
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "pathing.json"
            raw = source.read_text()
            code = pathing_tool.strip_comments(raw)
            poses = pathing_tool.parse_pose_constants(code)
            generated = pathing_tool.build_output(
                pathing_tool.resolve_runtime_pose_map(
                    poses,
                    alliance="blue",
                    location="far",
                    force_close_score1=False,
                    start_close_skip_far=False,
                ),
                pathing_tool.parse_paths(code),
                *pathing_tool.parse_follow_and_wait_sequence(code),
            )
            output.write_text(json.dumps(generated, indent=2) + "\n")

            self.assertEqual(generated, json.loads(output.read_text()))


if __name__ == "__main__":
    unittest.main()
