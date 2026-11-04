from flask import Blueprint, render_template

from ..services import text_processing

txt_bp = Blueprint(
    "txt",
    __name__,
    url_prefix="/txt",
)


@txt_bp.route("/replace")
def new_line():
    header_message = "改行表示画面"

    # ファイルのPath取得
    file_path = text_processing.get_input_file_path()

    # 対象ファイル取得 input.txt
    file_content = text_processing.read_input_file(file_path)

    # 保存処理
    saved_obj = text_processing.replace_characters(file_content)
    output_path = text_processing.get_output_one_path()

    text_processing.save_files(
        saved_obj,
        output_path,
    )

    return render_template(
        "text_processing/replace.html",
        header_message=header_message,
        replaced_result=saved_obj,
    )


@txt_bp.route("/regex")
def get_regex():
    header_message = "用語抽出画面"

    # ファイルのPath取得
    file_path = text_processing.get_input_file_path()

    # 対象ファイル取得 input.txt
    file_content = text_processing.read_input_file(file_path)

    # 正規表現
    regex_alphabet = text_processing.extract_regex(file_content)

    # 保存処理
    saved_obj = text_processing.join_regex(regex_alphabet)
    output_path = text_processing.get_output_two_path()

    text_processing.save_files(
        saved_obj,
        output_path,
    )

    # 重複除外の要素数カウント
    word_count = text_processing.count_regex_word(regex_alphabet)

    return render_template(
        "text_processing/regex.html",
        header_message=header_message,
        regex_list=regex_alphabet,
        word_count=word_count,
    )
