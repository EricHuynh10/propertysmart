import React, { useState, useEffect } from "react";
import axios from "axios";
import { Box, Typography, useMediaQuery, useTheme } from "@mui/material";
import TopSuburbsFilter from "./TopSuburbsFilter";
import TopSuburbsTable from "./TopSuburbsTable";

const TopSuburbsByYield = () => {
  const [top10, setTop10] = useState(null);
  const [stateValue, setStateValue] = useState('all');
  const [yieldValue, setYieldValue] = useState('rentalYield');
  const [propertyTypeValue, setPropertyTypeValue] = useState('all');
  const [remoteness, setRemotenessValue] = useState('0');
  const [totalRecords, setTotalRecords] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  const fetchTop10 = async () => {
    try {
      let url = `${process.env.REACT_APP_BACKEND_URL}/top10?state=${stateValue}&sortBy=${yieldValue}&propertyType=${propertyTypeValue}&remoteness=${remoteness}&page=${currentPage}`;
      const response = await axios.get(url);
      setTop10(response.data);
    } catch (error) {
      console.error('Error fetching top 10: ', error);
    }
  };

  const fetchTotalRecords = async () => {
    try {
      let url = `${process.env.REACT_APP_BACKEND_URL}/total-records?state=${stateValue}&sortBy=${yieldValue}&propertyType=${propertyTypeValue}&remoteness=${remoteness}`;
      const response = await axios.get(url);
      setTotalRecords(response.data.totalRecords);
    } catch (error) {
      console.error('Error fetching total records: ', error);
    }
  };

  useEffect(() => {
    fetchTop10();
  }, [stateValue, yieldValue, propertyTypeValue, remoteness, currentPage]);

  useEffect(() => {
    fetchTotalRecords();
  }, [stateValue, yieldValue, propertyTypeValue, remoteness]);

  return (
    <Box sx={{ flexDirection: 'column', marginTop : '1rem'}}>
      <Typography 
        variant="h2" 
        sx={{ 
          fontSize: isMobile? '1.2rem' : '1.5rem', 
          fontWeight: 'bold' 
        }}
      >
        Top Suburbs By Yield
      </Typography>
      <TopSuburbsFilter 
        setStateValue={setStateValue} 
        setYieldValue={setYieldValue} 
        setPropertyTypeValue={setPropertyTypeValue} 
        setRemotenessValue={setRemotenessValue}
      />
      <TopSuburbsTable 
        top10={top10} 
        totalRecords={totalRecords} 
        currentPage={currentPage} 
        setCurrentPage={setCurrentPage} 
      />
    </Box>
  );
}

export default TopSuburbsByYield;