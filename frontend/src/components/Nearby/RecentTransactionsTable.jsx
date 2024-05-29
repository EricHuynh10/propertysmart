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
  useMediaQuery,
  useTheme,
} from "@mui/material";
import { KeyboardArrowDown, KeyboardArrowUp } from "@mui/icons-material";

const CollapsibleRow = ({ transaction }) => {
  const [open, setOpen] = useState(false);
  const propertyUrl = `domain.com.au${transaction.url}`;

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
        <TableCell>
          <a href={`https://domain.com.au${transaction.url}`} target="_blank" rel="noopener noreferrer">
            {`${transaction.street}, ${transaction.suburb}, ${transaction.postcode}`}
          </a>
        </TableCell>
        <TableCell align="right">
          {transaction.price > 0 ? transaction.price.toLocaleString() : "-"}
        </TableCell>
        <TableCell align="right">
        {transaction.soldDate ? new Date(transaction.soldDate).toLocaleDateString('en-GB') : '-'}
        </TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            {transaction.propertyType == 'House' && (
              <Box margin={1}>
                Landsize: {transaction.landSize > 0 ? transaction.landSize.toLocaleString() : "-"} sqm<br />
              </Box>
            )}
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
};

const FullTable = ({ transactions }) => (
  <TableBody>
    {transactions && transactions.map((transaction, index) => {
      return (
        <TableRow key={index}>
          <TableCell>
            <a href={`https://domain.com.au${transaction.url}`} target="_blank" rel="noopener noreferrer">
              {`${transaction.street}, ${transaction.suburb}, ${transaction.postcode}`}
            </a>
          </TableCell>
          <TableCell align="right">{transaction.price > 0 ? transaction.price.toLocaleString() : "-"}</TableCell>
          <TableCell align="right">{transaction.soldDate ? new Date(transaction.soldDate).toLocaleDateString('en-GB') : '-'}</TableCell>
          <TableCell align="right">{transaction.landSize > 0 ? transaction.landSize.toLocaleString() : "-"} sqm</TableCell>
        </TableRow>
      )}
    )}
  </TableBody>
);

const RecentTransactionTable = ({ transactions }) => {
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
              <TableCell>Address</TableCell>
              {isMobile ? (
                <>
                  <TableCell align="right">Price</TableCell>
                  <TableCell align="right">Date</TableCell>
                </>
              ) : (
                <>
                  <TableCell align="right">Price</TableCell>
                  <TableCell align="right">Sold Date</TableCell>
                  <TableCell align="right">Landsize</TableCell>
                </>
              )}
            </TableRow>
          </TableHead>
          {isMobile ? (
            <TableBody>
              {transactions && transactions.map((transaction, index) => (
                <CollapsibleRow key={index} transaction={transaction} />
              ))}
            </TableBody>
          ) : (
            <FullTable transactions={transactions} />
          )}
        </Table>
      </TableContainer>
    </Box>
  );
};

export default RecentTransactionTable;