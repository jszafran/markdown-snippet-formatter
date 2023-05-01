import argparse
import re
from typing import Sequence

from black import format_str, Mode
from sqlfluff import fix

SUPPORTED_LANGUAGES = (
    "python",
    "sql",
)


def format_python_code(code: str) -> str:
    return format_str(code, mode=Mode())


def format_sql_code(code: str) -> str:
    return fix(code)


def format_match(match: re.Match) -> str:
    language = match.group(1)
    code = match.group(2)

    if language not in SUPPORTED_LANGUAGES:
        return match.group(0)

    format_func = {
        "python": format_python_code,
        "sql": format_sql_code,
    }.get(language)

    return f"```{language}\n{format_func(code.strip())}```"


def format_markdown_text(markdown: str) -> str:
    formatted_text = re.sub(
        r"```(.*?)\n(.*?)```",
        format_match,
        markdown,
        flags=re.DOTALL,
    )

    return formatted_text


def format_markdown(path: str) -> int:
    with open(path, "rt") as f:
        markdown_text = f.read()

    formatted_text = format_markdown_text(markdown_text)

    if markdown_text != formatted_text:
        with open(path, "wt") as f:
            f.write(formatted_text)
        print(f"Reformatted Python/SQL snippets in {path} file.")
        return 1
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    status = 0
    for filename in args.filenames:
        status = format_markdown(filename)

    return status


if __name__ == "__main__":
    raise SystemExit(main())
