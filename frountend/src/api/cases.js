import { apiRequest } from "./client";

export function analyzeCase(query) {
  return apiRequest("/api/cases/analyze", {
    method: "POST",
    body: JSON.stringify({ query }),
  });
}

export function searchCases({
  query,
  category,
  court,
  startDate,
  endDate,
  judgmentResult,
  page = 1,
  size = 10,
}) {
  return apiRequest("/api/cases/search", {
    method: "POST",
    body: JSON.stringify({
      query,
      category: category || null,
      court: court || null,
      start_date: startDate || null,
      end_date: endDate || null,
      judgment_result: judgmentResult || null,
      page,
      size,
    }),
  });
}

export function getCaseDetail(caseId) {
  return apiRequest(`/api/cases/${encodeURIComponent(caseId)}`);
}

export function getCaseSections(caseId) {
  return apiRequest(`/api/cases/${encodeURIComponent(caseId)}/sections`);
}

export function summarizeCase(caseId, forceRegenerate = false) {
  return apiRequest(`/api/cases/${encodeURIComponent(caseId)}/summary`, {
    method: "POST",
    body: JSON.stringify({ force_regenerate: forceRegenerate }),
  });
}

export function simplifyCase(
  caseId,
  sectionTypes = ["주문", "법원의 판단"],
  forceRegenerate = false,
) {
  return apiRequest(`/api/cases/${encodeURIComponent(caseId)}/simplify`, {
    method: "POST",
    body: JSON.stringify({
      section_types: sectionTypes,
      force_regenerate: forceRegenerate,
    }),
  });
}

export function getSimplifiedCase(caseId) {
  return apiRequest(`/api/cases/${encodeURIComponent(caseId)}/simplified`);
}

export function getCaseLegalTerms(caseId) {
  return apiRequest(`/api/cases/${encodeURIComponent(caseId)}/legal-terms`);
}

export function getSimilarCases(caseId) {
  return apiRequest(`/api/cases/${encodeURIComponent(caseId)}/similar`);
}
