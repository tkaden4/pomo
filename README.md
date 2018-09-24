# pomo

A command-line pomodoro tracker

(documentation)[https://www.tkaden.net/pomo]

## Installation (in Progress)
```bash
# APT
apt install pomo
# ... or pip
pip install pomo
```

## Usage

### Configuration (~/.pomorc)
```toml
[presets.default]
long_break = 00:20:00    # Length of a long break (after every <rollover> pomodoro)
short_break = 00:05:00   # Length of a short break
work_period = 00:25:00   # Amount of time per pomodoro
rollover = 4        # Number of pomodoros before taking long break

[presets.custom]
extend = "default"  # Extend the default preset
rollover = 3        # Use a smaller rollover
```