import { BrowserRouter, Routes, Route } from 'react-router-dom';
import DocLayout from './layout/DocLayout';
import Home from './pages/Home';
import GettingStarted from './pages/docs/GettingStarted';
import HermesDoc from './pages/docs/Hermes';
import CacheDoc from './pages/docs/Cache';
import CountriesDoc from './pages/docs/Countries';
import ExportDoc from './pages/docs/Export';
import WorldBankDoc from './pages/docs/WorldBank';
import IMFDoc from './pages/docs/IMF';
import GDELTDoc from './pages/docs/GDELT';
import OpenSanctionsDoc from './pages/docs/OpenSanctions';
import HDXCPIDoc from './pages/docs/HDXCPI';
import SchemasDoc from './pages/docs/Schemas';
import FeaturesDoc from './pages/docs/Features';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/docs" element={<DocLayout />}>
          <Route index element={<GettingStarted />} />
          <Route path="getting-started" element={<GettingStarted />} />
          <Route path="hermes" element={<HermesDoc />} />
          <Route path="cache" element={<CacheDoc />} />
          <Route path="countries" element={<CountriesDoc />} />
          <Route path="export" element={<ExportDoc />} />
          <Route path="world-bank" element={<WorldBankDoc />} />
          <Route path="imf" element={<IMFDoc />} />
          <Route path="gdelt" element={<GDELTDoc />} />
          <Route path="opensanctions" element={<OpenSanctionsDoc />} />
          <Route path="hdx-cpi" element={<HDXCPIDoc />} />
          <Route path="schemas" element={<SchemasDoc />} />
          <Route path="features" element={<FeaturesDoc />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
