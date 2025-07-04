# TODO

This is a toy TODO app for BE interviews.  The goal is to present a project that can be understood quickly by a back
end developer, even without Python experience.  The lack of authentication and user separation should be ignored, as
well as the lack of production database.  Everything else should be considered fair game for comment.

The app does actually run.

## Dependencies

- [uv](https://docs.astral.sh/uv/)

## Running

On a fresh checkout, intialize the venv:

```sh
uv venv
```

Run the dev server:

```sh
uv run fastapi dev
```

Browse to http://127.0.0.1:8000

Live docs can be found at http://127.0.0.1:8000/docs

## Running tests

```sh
uv run pytest
```
