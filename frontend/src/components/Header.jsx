import React from 'react';
import { Box, Typography } from '@mui/material';

const Header = () => {
  return (
    <Box component='header'>
    <Typography 
      variant='h1' 
      sx={{ 
        fontSize: '2rem',
        fontWeight: 'bold',
        textAlign: 'center', 
        padding: '1rem'
      }}
    >
      &#127968; Property Smart
    </Typography>
  </Box>
  );
}

export default Header;