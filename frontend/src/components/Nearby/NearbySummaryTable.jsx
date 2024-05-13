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

const CollapsibleRow = ({ type, data }) => {
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
        <TableCell>{type}</TableCell>
        <TableCell align="right">
          {data.medianPrice_L12M > 0 ? data.medianPrice_L12M.toLocaleString() : "-"}
        </TableCell>
        <TableCell align="right">
        {data.TranxLTM_L12M > 0 ? data.TranxLTM_L12M.toLocaleString() : "-"}
        </TableCell>
      </TableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box margin={1}>
              <strong>Median Price last year: </strong> {data.medianPrice_L12M_prev > 0 ? data.medianPrice_L12M_prev.toLocaleString() : "-"} <br />
              <strong># of Transactions: </strong> {data.TranxLTM_L12M_prev > 0 ? data.TranxLTM_L12M_prev.toLocaleString() : "-"} <br />
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
};

const FullTable = ({ nearbySummary }) => (
  <TableBody>
    {nearbySummary && Object.entries(nearbySummary).map(([key, value], index) => (
      <TableRow key={index}>
        <TableCell>{key}</TableCell>
        <TableCell align="right">{value.medianPrice_L12M > 0 ? value.medianPrice_L12M.toLocaleString() : "-"}</TableCell>
        <TableCell align="right">{value.TranxLTM_L12M > 0 ? value.TranxLTM_L12M.toLocaleString() : "-"}</TableCell>
        <TableCell align="right">{value.medianPrice_L12M_prev > 0 ? value.medianPrice_L12M_prev.toLocaleString() : "-"}</TableCell>
        <TableCell align="right">{value.TranxLTM_L12M_prev > 0 ? value.TranxLTM_L12M_prev.toLocaleString() : "-"}</TableCell>
      </TableRow>
    ))}
  </TableBody>
);

const NearbySummaryTable = ({ nearbySummary }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  return (
    <Box sx={{ mt: '1rem' }}>
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
              <TableCell>Type</TableCell>
              {isMobile ? (
                <>
                  <TableCell align="right">Median Price</TableCell>
                  <TableCell align="right"># Tranx</TableCell>
                </>
              ) : (
                <>
                  <TableCell align="right">Median Price</TableCell>
                  <TableCell align="right"># Transactions</TableCell>
                  <TableCell align="right">Median Price (last year)</TableCell>
                  <TableCell align="right"># Transactions (last year) </TableCell>
                </>
              )}
            </TableRow>
          </TableHead>
          {isMobile ? (
            <TableBody>
              {nearbySummary && Object.entries(nearbySummary).map(([key, value], index) => (
                <CollapsibleRow key={index} type={key} data={value} />
              ))}
            </TableBody>
          ) : (
            <FullTable nearbySummary={nearbySummary} />
          )}
        </Table>
      </TableContainer>
    </Box>
  );
};

export default NearbySummaryTable;