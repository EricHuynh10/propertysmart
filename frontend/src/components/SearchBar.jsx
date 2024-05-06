import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import axios from 'axios';
import { Box, Button } from '@mui/material';
import SearchStyles from './SearchBar.module.css'

const SearchBar = ({ setResult }) => {
  const [inputValue, setInputValue] = useState('');
  const [locationOptions, setLocationOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);

  const fetchLocationOptions = async (inputValue) => {
    try {
      let url = `${process.env.REACT_APP_BACKEND_URL}/location-options`;
      if (inputValue && inputValue !== '') {
        url += `?search=${inputValue}`;
      }
      const response = await axios.get(url);
      const options = response.data.map((location) => ({
        label: `${location.suburb}, ${location.state}, ${location.postcode}`,
        value: {
          suburb: location.suburb,
          state: location.state,
          postcode: location.postcode
        }
      }));
      setLocationOptions(options);
    } catch (error) {
      console.error('Error fetching location options: ', error);
    }
  };

  useEffect(() => {
    fetchLocationOptions();
  }, []);

  const handleInputChange = (newValue) => {
    setInputValue(newValue);
    setTimeout(() => {
      fetchLocationOptions(newValue);
    }, 300);
  };

  const handleChange = (option) => {
    setSelectedOption(option);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const selectedOptionString = selectedOption.value.suburb + '-' + selectedOption.value.state + '-' + selectedOption.value.postcode;
      const selectedOptionStringFormatted = selectedOptionString.replace(/\s+/g, '-').toLowerCase();
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/suburb/${selectedOptionStringFormatted}`);
      setResult(response.data);
    } catch (error) {
      console.error('Error fetching data: ', error);
    }
  };

  return (
    <Box className={SearchStyles.searchBarContainer}
    >
      <Select
        className={SearchStyles.searchBox}
        name="suburb"
        inputValue={inputValue}
        onInputChange={handleInputChange}
        onChange={handleChange}
        options={locationOptions}
        placeholder="Enter a suburb, state, postcode"
      />
      <Button onClick={handleSubmit} variant="contained" className={SearchStyles.searchButton}>Search</Button>
    </Box>
  );
};

export default SearchBar;