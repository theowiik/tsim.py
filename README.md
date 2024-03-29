# TSimPy (tsim.py) 🚂 [![Codacy Badge](https://app.codacy.com/project/badge/Grade/2ca50f04f6314d29b8271f5cbdbf4207)](https://app.codacy.com/gh/theowiik/train-sim/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

Simple train simulator

- [train-sim 🚂 ](#train-sim--)
  - [Features 🌟](#features-)
  - [Install 💾](#install-)
  - [Run 🏃](#run-)
  - [Format Files 📝](#format-files-)

## Features 🌟

Train simulator that:

- [x] uses MVC
  - [x] simulation is not based on framerate, and can be run at any speed
- [ ] is determenistic
- [x] is modern (Python 3.12+)
- [x] minimal dependencies
- [ ] property based testing
- [ ] easily editable rail network

## Install 💾

```bash
pip install -r requirements.txt
pre-commit install
```

## Run 🏃

```bash
python src/main.py
```

## Format Files 📝

Run all formatting automatically with kool.dev:

1. Install https://kool.dev
2. Run `kool run format`

