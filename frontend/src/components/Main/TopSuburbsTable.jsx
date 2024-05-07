import React, { useState } from "react";
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
  TableFooter,
  TablePagination,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import { KeyboardArrowDown, KeyboardArrowUp } from "@mui/icons-material";

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
        <TableCell>{row.suburb + ', ' + row.state}</TableCell>
        <TableCell align="right">
          {row.annualGrowth ? `${(row.annualGrowth * 100).toFixed(1)}%` : "-"}
        </TableCell>
        <TableCell align="right">
          {row.rentalYield ? `${(row.rentalYield * 100).toFixed(1)}%` : "-"}
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

const FullTable = ({ top10 }) => (
  <TableBody>
    {top10 && top10.map((row, index) => (
      <TableRow key={index}>
        <TableCell>{row.suburb}</TableCell>
        <TableCell align="right">{row.state}</TableCell>
        <TableCell align="right">{row.postcode}</TableCell>
        <TableCell align="right">{row.propertyType}</TableCell>
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

const TopSuburbsTable = ({
  top10,
  totalRecords,
  currentPage,
  setCurrentPage,
}) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  return (
    <Box sx={{ mt: '0.5rem' }}>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow
              sx={{
                backgroundColor: "#1976d2",
                "& .MuiTableCell-root": { color: "#fff", fontWeight: "bold" },
              }}
            >
              {isMobile && <TableCell></TableCell>}
              <TableCell>Suburb</TableCell>
              {!isMobile && <TableCell align="right">State</TableCell>}
              {isMobile ? (
                <>
                  <TableCell align="right">Price Growth</TableCell>
                  <TableCell align="right">Rental Yield</TableCell>
                </>
              ) : (
                <>
                  <TableCell align="right">Postcode</TableCell>
                  <TableCell align="right">Type</TableCell>
                  <TableCell align="right">Beds</TableCell>
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
              {top10 && top10.map((row, index) => (
                <CollapsibleRow key={index} row={row} />
              ))}
            </TableBody>
          ) : (
            <FullTable top10={top10} />
          )}
          <TableFooter>
            <TableRow>
              <TablePagination
                rowsPerPageOptions={[]}
                count={totalRecords}
                rowsPerPage={10}
                page={currentPage - 1}
                onPageChange={(e, newPage) => setCurrentPage(newPage + 1)}
              />
            </TableRow>
          </TableFooter>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default TopSuburbsTable;
