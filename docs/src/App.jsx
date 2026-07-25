import { BrowserRouter, Routes, Route } from 'react-router-dom';
import DocLayout from './layout/DocLayout';
import Home from './pages/Home';
import GettingStarted from './pages/docs/GettingStarted';
import HermesDoc from './pages/docs/Hermes';
import BaseConnectorDoc from './pages/docs/BaseConnector';
import CacheDoc from './pages/docs/Cache';
import CountriesDoc from './pages/docs/Countries';
import FredDoc from './pages/docs/Fred';
import BISDoc from './pages/docs/BIS';
import IMFDoc from './pages/docs/IMF';
import WorldBankDoc from './pages/docs/WorldBank';
import GDELTDoc from './pages/docs/GDELT';
import UCDPDoc from './pages/docs/UCDP';
import NewsAPIDoc from './pages/docs/NewsAPI';
import VDemDoc from './pages/docs/VDem';
import ComtradeDoc from './pages/docs/Comtrade';
import SchemasDoc from './pages/docs/Schemas';
import FeaturesDoc from './pages/docs/FeaturesDoc';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/docs" element={<DocLayout />}>
          <Route index element={<GettingStarted />} />
          <Route path="getting-started" element={<GettingStarted />} />
          <Route path="hermes" element={<HermesDoc />} />
          <Route path="base-connector" element={<BaseConnectorDoc />} />
          <Route path="cache" element={<CacheDoc />} />
          <Route path="countries" element={<CountriesDoc />} />
          <Route path="fred" element={<FredDoc />} />
          <Route path="bis" element={<BISDoc />} />
          <Route path="imf" element={<IMFDoc />} />
          <Route path="world-bank" element={<WorldBankDoc />} />
          <Route path="gdelt" element={<GDELTDoc />} />
          <Route path="ucdp" element={<UCDPDoc />} />
          <Route path="newsapi" element={<NewsAPIDoc />} />
          <Route path="v-dem" element={<VDemDoc />} />
          <Route path="comtrade" element={<ComtradeDoc />} />
          <Route path="schemas" element={<SchemasDoc />} />
          <Route path="features" element={<FeaturesDoc />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
