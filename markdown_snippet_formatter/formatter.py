import re

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

    return f"```{language}\n{format_func(code.strip())}\n```"


def format_markdown(path: str) -> None:
    with open(path, "rt") as f:
        markdown_text = f.read()

    formatted_text = re.sub(
        r"```(.*?)\n(.*?)```",
        format_match,
        markdown_text,
        flags=re.DOTALL,
    )

    if markdown_text != formatted_text:
        with open("formatting_result.md", "wt") as f:
            f.write(formatted_text)
        print("Formatted code")
        return
    print("Code was not formatted")
