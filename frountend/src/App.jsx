import { Route, Routes } from "react-router-dom";

import HomePage from "./pages/HomePage.jsx";
import CaseListPage from "./pages/CaseListPage.jsx";
import CaseDetailPage from "./pages/CaseDetailPage.jsx";
import LifeLawPage from "./pages/LifeLawPage.jsx";
import LegalTermsPage from "./pages/LegalTermsPage.jsx";
import CourtMapPage from "./pages/CourtMapPage.jsx";
import CommunityPage from "./pages/CommunityPage.jsx";

import SavedCasesPage from "./pages/SavedCasesPage.jsx";
import RecentCasesPage from "./pages/RecentCasesPage.jsx";
import NoticesPage from "./pages/NoticesPage.jsx";
import FaqPage from "./pages/FaqPage.jsx";
import CustomerServicePage from "./pages/CustomerServicePage.jsx";
import SettingsPage from "./pages/SettingsPage.jsx";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/cases" element={<CaseListPage />} />
      <Route path="/cases/:caseId" element={<CaseDetailPage />} />
      <Route path="/life-law" element={<LifeLawPage />} />
      <Route path="/legal-terms" element={<LegalTermsPage />} />
      <Route path="/court-map" element={<CourtMapPage />} />
      <Route path="/community" element={<CommunityPage />} />

      <Route path="/saved-cases" element={<SavedCasesPage />} />
      <Route path="/recent-cases" element={<RecentCasesPage />} />
      <Route path="/notices" element={<NoticesPage />} />
      <Route path="/faq" element={<FaqPage />} />
      <Route path="/customer-service" element={<CustomerServicePage />} />
      <Route path="/settings" element={<SettingsPage />} />
    </Routes>
  );
}

export default App;
