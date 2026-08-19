import argparse
import io
import json
import zipfile
from pathlib import Path


# --------------------------------------------------
# 문자열 정리
# --------------------------------------------------
def clean(value):
    if value is None:
        return ""
    return str(value).strip()


# --------------------------------------------------
# NIA 원본 JSON → CaseFinder에서 쓰기 쉬운 구조
# --------------------------------------------------
def convert_case(raw, source_file):
    info = raw.get("info", {})

    keywords = (
        info.get("keyword_tag", {})
        .get("keyword", [])
    )

    reference_info = info.get(
        "Reference_info",
        {}
    )

    return {
        # CaseFinder ID
        "case_id": (
            f"nia-{clean(info.get('caseNoID'))}"
            if info.get("caseNoID")
            else f"nia-{Path(source_file).stem}"
        ),

        # 사건번호
        "case_number": clean(
            info.get("caseNo")
        ),

        # 사건명
        "case_name": clean(
            info.get("caseNm")
        ),

        # 법원
        "court_name": clean(
            info.get("courtNm")
        ),

        # 법원 구분
        "court_type": clean(
            info.get("courtType")
        ),

        # 선고일
        "decision_date": clean(
            info.get("judmnAdjuDe")
        ),

        # 민사 / 형사 / 가사 등
        "category": clean(
            info.get("caseClass")
        ),

        # 판결 요지
        "summary": clean(
            info.get("jdgmn")
        ),

        # 핵심 키워드
        "main_issues": (
            keywords
            if isinstance(keywords, list)
            else []
        ),

        # 관련 법령
        "reference_rules": clean(
            reference_info.get(
                "reference_rules"
            )
        ),

        # 판결문 섹션
        "sections": raw.get(
            "sections",
            []
        ),

        # ZIP 내부 파일명
        "source_file": source_file,
    }


# --------------------------------------------------
# ZIP 안의 JSON 하나 읽기
# --------------------------------------------------
def load_json_from_zip(
    archive,
    member
):
    raw_bytes = archive.read(
        member
    )

    # 대부분 UTF-8
    try:
        text = raw_bytes.decode(
            "utf-8-sig"
        )

    # 혹시 CP949 데이터가 있을 경우
    except UnicodeDecodeError:
        text = raw_bytes.decode(
            "cp949"
        )

    return json.loads(text)


# --------------------------------------------------
# ZIP 내부 판례 순차 읽기
# --------------------------------------------------
def read_cases_from_zip(
    zip_path,
    category=None,
    limit=None
):
    zip_path = Path(zip_path)

    if not zip_path.exists():
        raise FileNotFoundError(
            f"ZIP 파일을 찾을 수 없습니다:\n"
            f"{zip_path}"
        )

    print()
    print("==============================")
    print("NIA 판결 데이터 ZIP 읽기")
    print("==============================")
    print(f"ZIP: {zip_path}")
    print()

    count = 0
    error_count = 0

    with zipfile.ZipFile(
        zip_path,
        "r"
    ) as archive:

        members = archive.infolist()

        json_members = [
            member
            for member in members

            if not member.is_dir()

            and member.filename.lower()
            .endswith(".json")
        ]

        print(
            f"ZIP 내부 JSON: "
            f"{len(json_members):,}개"
        )

        print()

        for member in json_members:

            # 예:
            # 01.일반판결/민사/xxxx.json
            member_name = (
                member.filename
            )

            # 특정 폴더만 읽고 싶을 때
            if category:

                normalized_path = (
                    member_name
                    .replace("\\", "/")
                )

                parts = (
                    normalized_path
                    .split("/")
                )

                if category not in parts:
                    continue

            try:
                raw = load_json_from_zip(
                    archive,
                    member
                )

                case = convert_case(
                    raw,
                    member_name
                )

                count += 1

                print(
                    f"[{count:05d}] "
                    f"{case['category']} | "
                    f"{case['court_name']} | "
                    f"{case['case_number']} | "
                    f"{case['case_name']}"
                )

                print(
                    f"         선고일: "
                    f"{case['decision_date']}"
                )

                print(
                    f"         요약: "
                    f"{case['summary'][:100]}"
                )

                print(
                    f"         키워드: "
                    f"{', '.join(case['main_issues'][:5])}"
                )

                print(
                    f"         관련법령: "
                    f"{case['reference_rules']}"
                )

                print()

                # 테스트용 제한
                if (
                    limit is not None
                    and count >= limit
                ):
                    break

            except Exception as e:

                error_count += 1

                print(
                    f"[ERROR] "
                    f"{member_name}"
                )

                print(
                    f"        "
                    f"{type(e).__name__}: "
                    f"{e}"
                )

    print()
    print("==============================")
    print("읽기 완료")
    print("==============================")
    print(
        f"정상 읽기: {count:,}개"
    )
    print(
        f"오류: {error_count:,}개"
    )


# --------------------------------------------------
# 실행
# --------------------------------------------------
def main():

    parser = argparse.ArgumentParser(
        description=(
            "NIA 판결서 ZIP을 "
            "압축 해제하지 않고 읽습니다."
        )
    )

    parser.add_argument(
        "zip_path",
        help="NIA ZIP 파일 경로"
    )

    parser.add_argument(
        "--category",
        default=None,
        help=(
            "특정 폴더만 읽기 "
            "예: 민사, 가사, 형사A"
        )
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=(
            "테스트할 판례 개수"
        )
    )

    args = parser.parse_args()

    read_cases_from_zip(
        zip_path=args.zip_path,
        category=args.category,
        limit=args.limit
    )


if __name__ == "__main__":
    main()