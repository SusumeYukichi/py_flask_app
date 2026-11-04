import re
from pathlib import Path

from flask import current_app


# ファイルのPath取得
def get_input_file_path():
    current_app.logger.info("input.txtのパス取得を開始します.")

    root_dir = Path(current_app.root_path)

    file_path = root_dir / "text_files" / "input" / "input.txt"

    current_app.logger.info("input.txtのパス取得が完了しました.")

    return file_path


# ファイルの取得
def read_input_file(file_path):
    current_app.logger.info("input.txtの読み込みを開始します.")

    file_content = file_path.read_text(encoding="utf-8")

    current_app.logger.info("input.txtの読み込みが完了しました.")

    return file_content


# 文字数カウント
def count_characters(file_content):
    content = file_content

    character_count = len(content)

    return character_count


# 置換 (記号→改行)
def replace_characters(file_content):
    content = file_content

    replaced_result = (
        content.replace("、", "\n").replace("。", "\n").replace("：", "\n")
    )

    return replaced_result


# 正規表現
def extract_regex(file_content):
    content = file_content

    regex_pattern = re.compile(r"[A-Za-z-]+")

    # list型生成(パターン無しの為)
    regex_alphabet = regex_pattern.findall(content)

    return regex_alphabet


# 1用語ごとに改行処理
def join_regex(regex_alphabet):
    content = regex_alphabet

    saved_obj = "\n".join(content)

    return saved_obj


# 正規表現済の要素数カウント
def count_regex_word(regex_alphabet):
    content = regex_alphabet

    # set型オブジェクトに変換
    set_obj = set(content)

    # 重複除外後の要素数をint型で取得
    word_count = len(set_obj)

    return word_count


# 保存先パス指定
def get_output_one_path():

    # ルートPathオブジェクト生成
    root_dir = Path(current_app.root_path)

    # 保存先のファイルパス生成
    output_path = root_dir / "instance" / "text_files" / "output_01.txt"

    return output_path


# 保存先パス指定
def get_output_two_path():

    # ルートPathオブジェクト生成
    root_dir = Path(current_app.root_path)

    # 保存先のファイルパス生成
    output_path = root_dir / "instance" / "text_files" / "output_02.txt"

    return output_path


# 保存処理
def save_files(
    saved_obj,
    output_path,
):
    current_app.logger.info("ファイル保存を開始します.")

    save_directory = output_path.parent

    save_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        saved_obj,
        encoding="utf-8",
    )

    current_app.logger.info("ファイル保存が完了しました.")
