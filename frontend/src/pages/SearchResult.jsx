import React, { useContext, useEffect } from "react";
import Header from "../components/Main/Header";
import SearchBar from "../components/Main/SearchBar";
import { Box, Typography, useMediaQuery, useTheme } from "@mui/material";
import { useParams } from "react-router-dom";
import { Context } from '../Context';
import axios from 'axios';
import MedianPriceYield from "../components/SearchResult/MedianPriceYield";
import Schools from "../components/SearchResult/Schools";

const SearchResult = () => {
  const { searchQuery, setSearchQuery, searchResult, setSearchResult } = useContext(Context);
  const { suburb } = useParams();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  // update searchQuery if differs from params
  useEffect(() => {
    if (suburb && searchQuery !== suburb) {
      const suburbArray = suburb.split('-');
      const postcode = suburbArray[suburbArray.length - 1];
      const state = suburbArray[suburbArray.length - 2];
      const suburbName = suburbArray.slice(0, -2).join(' ');
      const suburbObject = {
        label: suburbName + ', ' + state + ', ' + postcode,
        value: {
          suburb: suburbName,
          state: state,
          postcode: postcode
        }
      };
      setSearchQuery(suburbObject);
    }
  }, [suburb]);

  const fetchSearchResult = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/suburb/${suburb}`);
      setSearchResult(response.data);
    } catch (error) {
      console.error('Error fetching search result: ', error);
    }
  };

  useEffect(() => {
    fetchSearchResult(searchQuery);
  }, [searchQuery]);

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <Header />
      <SearchBar />
      <Box
        component={'main'}
        sx={{
          display: "flex",
          flexDirection: "column",
          width: "fit-content",
          minWidth: "65%",
          mb: '1rem',
        }}>
        <Typography variant="h2" 
          sx={{ 
            mt: '1rem', 
            fontSize: isMobile? '1.2rem' : '1.5rem', 
            fontWeight: 'bold' 
          }}
        >
          {searchQuery.label}
        </Typography>
        {searchResult && searchResult.properties && (
          <MedianPriceYield />
        )}
        {searchResult && searchResult.schools && (
          <Schools />
        )}
      </Box>
    </Box>
  );
};

export default SearchResult;