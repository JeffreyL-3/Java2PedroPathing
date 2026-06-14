# Java2PedroPathing

Java2PedroPathing converts FTC autonomous Java source into JSON that can be
opened in the Pedro Pathing visualizer.

## Requirements

- Python 3.9 or newer
- An FTC autonomous Java file using the supported `Pose`, `Path`, `BezierLine`,
  `buildPath`, `FollowPath`, and `Delay` patterns shown in `examples/` and
  `samples/`

The converter uses Python's standard library and has no runtime dependencies.

## Install

Run directly from a clone:

```bash
python pathing_tool.py --help
```

Or install the command locally:

```bash
python -m pip install .
java2pedro-pathing --help
```

## Usage

```bash
java2pedro-pathing \
  --input examples/ANewWorkingAuto.java \
  --output blue_far_pathing.json \
  --alliance blue \
  --location far
```

Available options:

- `--alliance {blue,red}` selects the alliance and mirrors blue poses for red.
- `--location {far,close}` selects the starting and general scoring poses.
- `--force-close-score1` uses the close scoring pose for `scorePose1`.
- `--start-close-skip-far` uses `targetExitPosCloseBlue` for a close start.
- Use `--input -` to read Java source from standard input.

## Repository Layout

- `pathing_tool.py`: supported converter and command-line entry point
- `examples/`: primary example input
- `samples/`: additional supported source patterns and generated outputs
- `blue_far_pathing.json`: generated output for the primary example
- `PathingFileGenerator.java`: legacy, fixed Blue/Far JSON generator
- `tests/`: checks that committed generated artifacts remain reproducible

## Reproduce Generated Files

```bash
python pathing_tool.py --input examples/ANewWorkingAuto.java --output blue_far_pathing.json --alliance blue --location far
python pathing_tool.py --input samples/provided_working_code.java --output samples/provided_blue_far.json --alliance blue --location far
python pathing_tool.py --input samples/updated_auto.java --output samples/updated_blue_far.json --alliance blue --location far
```

## Development

Run the test suite before publishing changes:

```bash
python -m unittest discover -v
```

Build distributable Python artifacts:

```bash
python -m build
```

`PathingFileGenerator.java` uses text blocks and records, so it requires Java
16 or newer to compile. It is retained as a legacy fixed-output example; the
Python converter is the supported tool.
