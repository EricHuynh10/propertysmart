import React, { useState, useContext } from "react";
import {
  Box,
  Collapse,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import { KeyboardArrowDown, KeyboardArrowUp } from "@mui/icons-material";
import { Context } from '../../Context';

const CollapsibleRow = ({ row }) => {
  const [open, setOpen] = useState(false);

  return (
    <>
      <TableRow>
        <TableCell sx={{ padding: '0rem 0rem' }}>
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUp /> : <KeyboardArrowDown />}
          </IconButton>
        </TableCell>
        <TableCell>{row.propertyType}</TableCell>
        <TableCell align="right">{row.beds}</TableCell>
        <TableCell align="right">{row.medianPrice ? row.medianPrice.toLocaleString() : "-"}</TableCell>
        <TableCell align="right">
          {row.annualGrowth ? `${(row.annualGrowth * 100).toFixed(1)}%` : "-"}
        </TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box margin={1}>
              <strong>Postcode:</strong> {row.postcode} <br />
              <strong>Type:</strong> {row.propertyType} <br />
              <strong>Beds:</strong> {row.beds} <br />
              <strong>Median Price:</strong>{" "}
              {row.medianPrice ? row.medianPrice.toLocaleString() : "-"} <br />
              <strong>Total Yield:</strong>{" "}
              {row.totalYield ? `${(row.totalYield * 100).toFixed(1)}%` : "-"}{" "}
              <br />
              <strong>Sold L12M:</strong>{" "}
              {row.soldThisYear ? row.soldThisYear.toLocaleString() : "-"}
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
};

const FullTable = ({ results }) => (
  <TableBody>
    {results && results.map((row, index) => (
      <TableRow key={index}>
        <TableCell>{row.propertyType}</TableCell>
        <TableCell align="right">{row.beds}</TableCell>
        <TableCell align="right">
          {row.medianPrice ? row.medianPrice.toLocaleString() : "-"}
        </TableCell>
        <TableCell align="right">
          {row.annualGrowth ? `${(row.annualGrowth * 100).toFixed(1)}%` : "-"}
        </TableCell>
        <TableCell align="right">
          {row.rentalYield ? `${(row.rentalYield * 100).toFixed(1)}%` : "-"}
        </TableCell>
        <TableCell align="right">
          {row.totalYield ? `${(row.totalYield * 100).toFixed(1)}%` : "-"}
        </TableCell>
        <TableCell align="right">
          {row.soldThisYear ? row.soldThisYear.toLocaleString() : "-"}
        </TableCell>
      </TableRow>
    ))}
  </TableBody>
);


const MedianPriceYield = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const { searchResult } = useContext(Context);

  return (
    <Box sx={{ mt: '1rem', width: 'fit-content' }}>
      <Typography variant='h3' sx={{ fontSize: '1rem', fontWeight: 'bold' }}>
        Median Price and Yield
      </Typography>
      {searchResult && searchResult.properties && (
        <TableContainer component={Paper} sx={{ display: 'flex', width: 'auto' }}>
          <Table size="small">
            <TableHead>
              <TableRow
                sx={{
                  backgroundColor: "#1976d2",
                  "& .MuiTableCell-root": { color: "#fff", fontWeight: "bold" },
                }}
              >
                {isMobile && <TableCell></TableCell>}
                <TableCell>Type</TableCell>
                <TableCell align="right">Beds</TableCell>
                {isMobile ? (
                  <>
                    <TableCell align="right">Median Price</TableCell>
                    <TableCell align="right">Price Growth</TableCell>
                  </>
                ) : (
                  <>
                    <TableCell align="right">Median Price</TableCell>
                    <TableCell align="right">Price Growth</TableCell>
                    <TableCell align="right">Rental Yield</TableCell>
                    <TableCell align="right">Total Yield</TableCell>
                    <TableCell align="right">Sold L12M</TableCell>
                  </>
                )}
              </TableRow>
            </TableHead>
            {isMobile ? (
              <TableBody>
                {searchResult && searchResult.properties && searchResult.properties.map((row, index) => (
                  <CollapsibleRow key={index} row={row} />
                ))}
              </TableBody>
            ) : (
              <FullTable results={searchResult.properties} />
            )}
          </Table>
        </TableContainer>
      )}
    </Box>
  );
};

export default MedianPriceYield;
