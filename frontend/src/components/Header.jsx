import React from 'react';
import { Box, Typography, useTheme, useMediaQuery } from '@mui/material';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import homeImage from '../assets/home.png';

const Header = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  return (
    <Box component='header' 
      sx={{
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <img 
        src={homeImage} 
        alt='logo' 
        style={{ 
          width: 'auto', 
          height: isMobile ? '1.5rem' : '2.5rem'
        }} 
      />
      <Typography 
        variant='h1' 
        sx={{ 
          fontSize: isMobile? '1.5rem' : '2.5rem',
          fontWeight: 'bold',
          textAlign: 'center', 
          padding: '1rem 0.5rem'
        }}
      >
        Property Smart
      </Typography>
    </Box>
  );
}

export default Header;