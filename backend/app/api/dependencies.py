from fastapi import Request

from app.providers.base_case_provider import CaseProvider


def get_case_provider(request: Request) -> CaseProvider:
    return request.app.state.case_provider
