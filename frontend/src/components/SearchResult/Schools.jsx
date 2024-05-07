import React, { useState, useContext } from "react";
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import { Context } from '../../Context';

const Schools = () => {
  const { searchResult } = useContext(Context);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  return (
    <Box sx={{ mt: '1rem', width: 'fit-content' }}>
      <Typography variant='h3' sx={{ fontSize: '1rem', fontWeight: 'bold' }}>
        Schools
      </Typography>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow
              sx={{
                backgroundColor: "#1976d2",
                "& .MuiTableCell-root": { color: "#fff", fontWeight: "bold" },
              }}
            >
              <TableCell>School</TableCell>
              <TableCell align="right">School</TableCell>
              <TableCell align="right">Level</TableCell>
              <TableCell align="right">Score</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {searchResult && searchResult.schools && searchResult.schools.map((school, index) => (
              <TableRow key={index}>
                <TableCell>{school.school}</TableCell>
                <TableCell align="right">
                  {isMobile ? `${school.schoolType.substring(0, 3)}` : school.schoolType}
                </TableCell>
                <TableCell align="right">{school.educationLevel}</TableCell>
                <TableCell align="right">{school.score ? school.score : '-'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default Schools;