import React, { useState } from "react";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import TopSuburbsByYield from "../components/TopSuburbsByYield";
import { Box } from "@mui/material";

const Main = () => {
  const [result, setResult] = useState(null);
  return (
    <Box 
      id='main'
      sx={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        width: '100%',
        justifyContent: 'space-around',
        alignItems: 'center',
      }}
    >
      <Box 
        sx={{ display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
        flex: '1',
        }}
      >
        <Header />
        <SearchBar setResult={setResult} />
      </Box>
      <Box 
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start',
          width: '100%',
          flex: '4',
        }}
      >
        <TopSuburbsByYield />
      </Box>
    </Box>
  );
};

export default Main;