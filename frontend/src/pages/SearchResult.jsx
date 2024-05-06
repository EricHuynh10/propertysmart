import React, { useState } from "react";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import TopSuburbsByYield from "../components/TopSuburbsByYield";
import { Box } from "@mui/material";
import { useParams } from "react-router-dom";

const SearchResult = () => {
  const [result, setResult] = useState(null);
  const { suburb } = useParams();
  console.log(suburb);

  return (
    <Box>
      <Header />
      <SearchBar setResult={setResult} />
      {result && result.properties && (
        <TopSuburbsByYield properties={result.properties} />
      )}
    </Box>
  );
};

export default SearchResult;