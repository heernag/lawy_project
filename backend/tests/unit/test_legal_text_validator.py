from app.validators.legal_text_validator import LegalTextValidator


def test_validator_detects_changed_amount():
    validator = LegalTextValidator()
    result = validator.validate(
        "피고는 원고에게 5,000,000원을 지급하라.",
        "피고는 원고에게 3,000,000원을 지급해야 합니다.",
    )

    assert result.status == "review_required"
    assert "금액" in result.warnings[0]


def test_validator_passes_preserved_date_and_rate():
    validator = LegalTextValidator()
    result = validator.validate(
        "2025년 3월 1일부터 연 12%의 비율로 계산한 돈을 지급하라.",
        "2025년 3월 1일부터 연 12%의 지연이자를 지급해야 합니다.",
    )

    assert result.status == "passed"


def test_validator_detects_swapped_parties():
    validator = LegalTextValidator()
    result = validator.validate(
        "피고는 원고에게 돈을 지급하라.",
        "원고는 피고에게 돈을 지급해야 합니다.",
    )

    assert result.status == "review_required"
    assert any("원고와 피고" in warning for warning in result.warnings)
