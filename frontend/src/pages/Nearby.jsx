import React, { useEffect, useState } from "react";
import axios from 'axios';
import Header from "../components/Main/Header";
import { Box, Typography, useMediaQuery, useTheme, Link } from "@mui/material";
import NearbyTabs from "../components/Nearby/NearbyTabs";
import { useNavigate } from "react-router-dom";

const Nearby = () => {
  const [location, setLocation] = useState(null);
  const [nearbyTransactions, setNearbyTransactions] = useState([]);
  const [nearbySummary, setNearbySummary] = useState({});
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const [suburbCount, setSuburbCount] = useState({});
  const [dominatingSuburb, setDominatingSuburb] = useState('');
  const navigate = useNavigate();

  // get the current location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        setLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
      });
    } else {
      console.log("Geolocation is not supported by this browser.");
    }
  }, []);

  // find the suburb dominating transactions
  useEffect(() => {
    if (nearbyTransactions.length > 0) {
      const suburbCountCalc = nearbyTransactions.reduce((acc, transaction) => {
        const suburbString = transaction.suburb + ', ' + transaction.state + ', ' + transaction.postcode;
        if (acc[suburbString]) {
          acc[suburbString] += 1;
        }
        else {
          acc[suburbString] = 1;
        }
        return acc;
      });
      setSuburbCount(suburbCountCalc);
    }
  }, [nearbyTransactions]);
  useEffect(() => {
    if (suburbCount && Object.keys(suburbCount).length > 0) {
      const suburb = Object.keys(suburbCount).reduce((a, b) => suburbCount[a] > suburbCount[b] ? a : b);
      setDominatingSuburb(suburb);
    }
  }, [suburbCount])

  // fetch nearby summary
  useEffect(() => {
    if (location) {
      axios.get(`${process.env.REACT_APP_BACKEND_URL}/nearby?lat=${location.latitude}&lng=${location.longitude}`)
        .then((response) => {
          setNearbySummary(response.data.summary);
          setNearbyTransactions(response.data.transactions);
        })
        .catch((error) => {
          console.error('Error fetching nearby places', error);
        });
    }
  }, [location]);


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
        gap: '1rem',
      }}
    >
      <Box 
        sx={{ display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center',
        justifyContent: 'center',
        width: '100%',
        }}
      >
        <Header />
      </Box>
      <Box 
        sx={{
          display: 'flex',
          flexDirection: 'column',
          // alignItems: 'center',
          justifyContent: 'flex-start',
          width: '100%',
          flex: '1',
        }}
      >
        <Typography variant="h2" 
          sx={{ 
            fontSize: isMobile ? '1rem' : '1.5rem', 
            fontWeight: 'bold' 
          }}
        >
          Current Location
        </Typography>
        <Typography variant="body">
          {location ? `Lng: ${location.latitude}, Lat: ${location.longitude}` : "Unknown"}. 
          You are at suburb&nbsp;
          <Link
            sx={{ cursor: 'pointer' }}
            onClick={() => {
              if (dominatingSuburb) {
                let suburbString = dominatingSuburb.split(', ').join('-').replace(/ /g, '-');
                navigate(`/propertysmart/suburb/${suburbString.toLowerCase()}`);
              }
            }}
          >
            {dominatingSuburb ? dominatingSuburb : 'Unknown'}
          </Link>.
        </Typography>
        <NearbyTabs nearbySummary={nearbySummary} transactions={nearbyTransactions}/>
      </Box>
    </Box>
  );
};

export default Nearby;