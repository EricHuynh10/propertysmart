import React, { useState, useEffect, useContext } from 'react';
import Select from 'react-select';
import axios from 'axios';
import { Box, useTheme, useMediaQuery, Typography, Link } from '@mui/material';
import SearchStyles from './SearchBar.module.css'
import { useNavigate } from 'react-router-dom';
import { Context } from '../../Context';

const SearchBar = ({ setResult }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const [inputValue, setInputValue] = useState('');
  const [locationOptions, setLocationOptions] = useState([]);
  const navigate = useNavigate();
  const { searchQuery, setSearchQuery } = useContext(Context);

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

  const handleChange = async (option) => {
    setSearchQuery(option);
    try {
      const selectedOptionString = option.value.suburb + '-' + option.value.state + '-' + option.value.postcode;
      const selectedOptionStringFormatted = selectedOptionString.replace(/\s+/g, '-').toLowerCase();
      navigate(`/propertysmart/suburb/${selectedOptionStringFormatted}`);
    } catch (error) {
      console.error('Error fetching data: ', error);
    }
  };

  return (
    <Box 
      sx={{
        display: 'flex',
        flexDirection: 'column', 
        width: '100%', 
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Box className={SearchStyles.searchBarContainer}>
        <Select
          className={SearchStyles.searchBox}
          name="suburb"
          inputValue={inputValue}
          onInputChange={handleInputChange}
          onChange={handleChange}
          options={locationOptions}
          value={searchQuery}
          placeholder="Enter a suburb, state, postcode"
        /> 
      </Box>
      <Box
        onClick={() => navigate('/propertysmart/nearby')}
        sx={{
          width: '65%',
          cursor: 'pointer',
          minWidth: '300px',
        }}
      >
        <Link>
          or Use your current location
        </Link>
      </Box>
    </Box>
  );
};

export default SearchBar;