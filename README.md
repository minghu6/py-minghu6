# An Utils Package

## Environment Setup

### 1. Configure Shell Environment Variables

Add these lines in your bash startup profile.

```bash
export MINGHU6_HOME="<actual-dir-path>/py-minghu6"

export PATH="$PATH:$MINGHU6_HOME/src/minghu6/tools/bin"

# Optional: load bash completions
for file in $(pym6 find -p $MINGHU6_HOME/src/minghu6/tools/bash-completion/ '*'); do
    . $file
done
```

### 2. Install Required Tools (mise + uv)

This project uses [`mise`](https://mise.jdx.dev) to manage the tasks and
[`uv`](https://docs.astral.sh/uv) for Python project management.

### 3. Install Project Dependencies

```bash
cd $MINGHU6_HOME && uv sync
```


## Usage

### Run Tools

```bash
pym6 <command> <arguments>...
```

### Other Usage

reference the `.mise.toml`
