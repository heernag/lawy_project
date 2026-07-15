from app.core import errors


def test_all_error_codes_exports_stable_frontend_contract():
    assert errors.ALL_ERROR_CODES == (
        errors.INVALID_REQUEST,
        errors.CASE_NOT_FOUND,
        errors.CASE_PROVIDER_ERROR,
        errors.SEARCH_FAILED,
        errors.SIMPLIFICATION_FAILED,
        errors.VALIDATION_FAILED,
        errors.RATE_LIMIT_EXCEEDED,
        errors.INTERNAL_SERVER_ERROR,
    )
