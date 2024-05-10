import React, { useState } from 'react';
import AppStyles from './App.module.css';
import Main from './pages/Main';
import SearchResult from './pages/SearchResult';
import Nearby from './pages/Nearby';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; 
import { Context } from './Context';
import { Box } from '@mui/material';
import { useAnalytics } from 'react-ga4';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResult, setSearchResult] = useState('');
  useAnalytics('G-PW7QTQNG2C');

  const contextValue = { 
    searchQuery,
    setSearchQuery,
    searchResult,
    setSearchResult,
  };

  return (
    <Box className={AppStyles.App}>
      <Context.Provider value={contextValue}>
        <Router>
          <Routes>
              <Route path="/propertysmart" element={<Main />} />
              <Route path="/propertysmart/*" element={<Main />} />
              <Route path="/propertysmart/main" element={<Main />} />
              <Route path="/propertysmart/suburb/:suburb" element={<SearchResult />} />
              <Route path="/propertysmart/nearby" element={<Nearby />} />
            </Routes>
        </Router>
      </Context.Provider>
    </Box>
  )
};

export default App;
