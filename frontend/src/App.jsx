import React, { useState } from 'react';
import AppStyles from './App.module.css';
import Main from './pages/Main';
import SearchResult from './pages/SearchResult';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; 
import { Context } from './Context';
import { Box } from '@mui/material';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResult, setSearchResult] = useState('');

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
              <Route path="/" element={<Main />} />
              <Route path="*" element={<Main />} />
              <Route path="/main" element={<Main />} />
              <Route path="/suburb/:suburb" element={<SearchResult />} />
            </Routes>
        </Router>
      </Context.Provider>
    </Box>
  )
};

export default App;
