import React from "react";
import { Box, Select, MenuItem, FormControl, InputLabel } from "@mui/material";

const TopSuburbsFilter = ({ setStateValue, setYieldValue, setPropertyTypeValue, setRemotenessValue }) => {
  const states = {
    'all': 'All States',
    'act': 'ACT',
    'nsw': 'NSW',
    'nt': 'NT',
    'qld': 'QLD',
    'sa': 'SA',
    'tas': 'TAS',
    'vic': 'VIC',
    'wa': 'WA'
  };

  const yieldTypes = {
    'rentalYield': 'Rental Yield',
    'annualGrowth': 'Price Growth',
    'totalYield': 'Total Yield'
  };

  const propertyTypes = {
    'all': 'All House Types',
    'house': 'House',
    'unit': 'Apartment'
  };

  const remotenessTypes = {
    '0': 'Major Cities of Australia',
    '1': 'Inner Regional Australia',
    '2': 'Outer Regional Australia',
    '3': 'Remote Australia',
    '4': 'Very Remote Australia',
    'all': 'All Regions'
  };

  const handleStateChange = (event) => {
    setStateValue(event.target.value);
  };

  const yieldTypeChange = (event) => {
    setYieldValue(event.target.value);
  };

  const handlePropertyTypeChange = (event) => {
    setPropertyTypeValue(event.target.value);
  };

  const handleRemotenessChange = (event) => {
    setRemotenessValue(event.target.value);
  };

  return (
    <Box 
      sx={{
        display: 'flex',
        flexDirection: 'row',
        flexWrap: 'wrap',
        marginTop : '0.5rem',
        marginLeft: '0.1rem',
        gap: '0.2rem'
      }}
    >
      <select onChange={handleStateChange} style={{ border: '1px solid lightgrey', borderRadius: '3px' }}>
        {Object.entries(states).map(([key, state]) => (
          <option key={key} value={key}>{state}</option>
        ))}
      </select>
      <select onChange={yieldTypeChange} style={{ border: '1px solid lightgrey', borderRadius: '3px' }}>
        {Object.entries(yieldTypes).map(([key, type]) => (
          <option key={key} value={key}>{type}</option>
        ))}
      </select>
      <select onChange={handlePropertyTypeChange} style={{ border: '1px solid lightgrey', borderRadius: '3px' }}>
        {Object.entries(propertyTypes).map(([key, type]) => (
          <option key={key} value={key}>{type}</option>
        ))}
      </select>
      <select onChange={handleRemotenessChange} style={{ border: '1px solid lightgrey', borderRadius: '3px' }}>
        {Object.entries(remotenessTypes).map(([key, type]) => (
          <option key={key} value={key}>{type}</option>
        ))}
      </select>
    </Box>    
  );
}

export default TopSuburbsFilter;