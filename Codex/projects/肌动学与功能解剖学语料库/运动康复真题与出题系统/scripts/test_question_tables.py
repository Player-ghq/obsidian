import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory


def load_module():
    spec = importlib.util.spec_from_file_location("build_question_tables", "work/build_question_tables.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_keeps_implicit_first_question_score_and_image_source():
    b = load_module()
    with TemporaryDirectory() as td:
        root = Path(td)
        ocr = root / "work" / "ocr" / "2025"
        img = root / "work" / "extracted" / "2025" / "pics"
        ocr.mkdir(parents=True)
        img.mkdir(parents=True)
        txt = ocr / "qq052001-18.txt"
        image = img / "qq052001-18.webp"
        image.write_bytes(b"fake")
        txt.write_text(
            "\n".join(
                [
                    "25考研专业课真题（回忆版）",
                    "上海体育大学运动康复学",
                    "615运动康复学专业基础综合",
                    "解剖：（简答题2*25，论述题1*50，共100分）",
                    "、简述踝关节的结构，运动形式，及参与运动的主要肌肉（25分）",
                    "二、简述人体骨杠杆的类型及在运动训练中的应用（25分）",
                    "三、仰卧起坐动作分析（50分）",
                ]
            ),
            encoding="utf-8",
        )
        records = b.parse_file(txt, "2025", workspace_root=root)
    assert len(records) == 3
    assert records[0]["question_text"].startswith("简述踝关节")
    assert records[0]["score"] == "25"
    assert records[0]["source_image"].endswith("work/extracted/2025/pics/qq052001-18.webp")
    assert records[2]["subject"] == "解剖"
    assert records[2]["score"] == "50"


def test_parse_section_score_when_question_line_has_no_points():
    b = load_module()
    with TemporaryDirectory() as td:
        root = Path(td)
        ocr = root / "work" / "ocr" / "2024"
        img = root / "work" / "extracted" / "2024" / "pics"
        ocr.mkdir(parents=True)
        img.mkdir(parents=True)
        txt = ocr / "qq915838-7.txt"
        (img / "qq915838-7.webp").write_bytes(b"fake")
        txt.write_text(
            "\n".join(
                [
                    "2024考研专业课真题（回忆版）",
                    "上海体育大学运动康复学",
                    "615医学技术（康复学）专业基础综合",
                    "生理：3题，共100分",
                    "简答题：2题*25分",
                    "1.什么是内环境稳态",
                    "论述题：1题*50分",
                    "2.简述激素的作用机制",
                ]
            ),
            encoding="utf-8",
        )
        records = b.parse_file(txt, "2024", workspace_root=root)
    assert records[0]["score"] == "25"
    assert records[1]["score"] == "50"


def test_parse_2023_header_and_png_source():
    b = load_module()
    with TemporaryDirectory() as td:
        root = Path(td)
        ocr = root / "work" / "ocr" / "2023"
        img = root / "work" / "extracted" / "2023" / "pics"
        ocr.mkdir(parents=True)
        img.mkdir(parents=True)
        txt = ocr / "qq370571-0.txt"
        (img / "qq370571-0.png").write_bytes(b"fake")
        txt.write_text(
            "\n".join(
                [
                    "2023考研专业课真题（回忆版）",
                    "上海体育大学运动康复学",
                    "615运动康复学专业基础综合",
                    "解剖：简答题2*25分",
                    "1.简述膝关节的构造和运动",
                ]
            ),
            encoding="utf-8",
        )
        records = b.parse_file(txt, "2023", workspace_root=root)
    assert len(records) == 1
    assert records[0]["year"] == "2023"
    assert records[0]["score"] == "25"
    assert records[0]["source_image"].endswith("work/extracted/2023/pics/qq370571-0.png")


def test_parse_2023_grade_header_and_bare_trailing_score():
    b = load_module()
    with TemporaryDirectory() as td:
        root = Path(td)
        ocr = root / "work" / "ocr" / "2023"
        img = root / "work" / "extracted" / "2023" / "pics"
        ocr.mkdir(parents=True)
        img.mkdir(parents=True)
        txt = ocr / "qq370571-11.txt"
        (img / "qq370571-11.png").write_bytes(b"fake")
        txt.write_text(
            "\n".join(
                [
                    "2023级上海体育学院运动康复真题",
                    "(回忆版)",
                    "1.骨骼的结构及运动锻炼对骨骼的影响25",
                    "2.内囊的位置，神经束的分布及损伤后的影响25分",
                ]
            ),
            encoding="utf-8",
        )
        records = b.parse_file(txt, "2023", workspace_root=root)
    assert len(records) == 2
    assert records[0]["school_track"] == "2023级上海体育学院运动康复真题"
    assert records[0]["subject"] == "解剖"
    assert records[0]["question_text"] == "骨骼的结构及运动锻炼对骨骼的影响"
    assert records[0]["score"] == "25"
    assert records[1]["score"] == "25"


if __name__ == "__main__":
    test_parse_keeps_implicit_first_question_score_and_image_source()
    test_parse_section_score_when_question_line_has_no_points()
    test_parse_2023_header_and_png_source()
    test_parse_2023_grade_header_and_bare_trailing_score()
