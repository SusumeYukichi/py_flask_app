def format_japanese_date(value):

    weekdays = [
        "月",
        "火",
        "水",
        "木",
        "金",
        "土",
        "日",
    ]

    if value is None:
        return ""

    return f"{value.month}/{value.day} ({weekdays[value.weekday()]})"


def capitalize_if_lower(value):

    if value and value.islower():
        return value.capitalize()

    return value


def capitalize_first_line(value):

    if not value:
        return value

    lines = value.splitlines()

    if lines and lines[0].islower():
        lines[0] = lines[0].capitalize()

    return "\n".join(lines)


# カスタムフィルター登録
def register_filters(app):
    app.add_template_filter(
        format_japanese_date,
        "jp_weekly",
    )
    app.add_template_filter(
        capitalize_if_lower,
        "capitalize_if_lower",
    )
    app.add_template_filter(
        capitalize_first_line,
        "capitalize_first_line",
    )
