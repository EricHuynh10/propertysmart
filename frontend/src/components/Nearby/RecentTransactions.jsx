import React, { useEffect, useState } from "react";
import { Box, Typography, FormControl, Select, MenuItem, InputLabel } from "@mui/material";
import RecentTransactionTable from "./RecentTransactionsTable";

const RecentTransactions = ({ transactions }) => {
  // get all combination of house types and beds from transactions
  const propertyTypes = transactions.map((transaction) => {
    return `${transaction.propertyType},${transaction.beds}`
  })
  const propertyTypesUnique = [...new Set(propertyTypes)]

  // create a dictionary of house types and available beds
  const propertyTypesDict = {}
  propertyTypesUnique.forEach((element) => {
    const [type, beds] = element.split(',')
    if (type === '-1' || beds === '-1') {
      return
    }
    if (type in propertyTypesDict) {
      propertyTypesDict[type].push(beds)
    } else {
      propertyTypesDict[type] = [beds]
    }
  })
  Object.keys(propertyTypesDict).forEach((type) => {
    propertyTypesDict[type].sort((a, b) => a - b)
  })

  const [propertyType, setPropertyType] = useState('')
  const [beds, setBeds] = useState('')
  const [filteredTransactions, setFilteredTransactions] = useState([])

  useEffect(() => {
    if (propertyTypesUnique) {
      // check if any element in houseTypes contains 'House'
      const defaultHouseType = propertyTypesUnique.find((type) => type.includes('House'))
      if (defaultHouseType) {
        const [type, beds] = defaultHouseType.split(',')
        setPropertyType(type)
        setBeds(beds)
      } else {
        const [type, beds] = propertyTypesUnique[0].split(',')
        setPropertyType(type)
        setBeds(beds)
      }
    }
  }, [])

  useEffect(() => {
    if (propertyType && beds) {
      const filtered = transactions.filter((transaction) => {
        return transaction.propertyType == propertyType && transaction.beds == beds
      })
      setFilteredTransactions(filtered)
    }
  }, [propertyType, beds])

  return (
    <Box>
      <Box sx={{ mt: '0.5rem' }}>
        <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
          <InputLabel id="property-type">Type</InputLabel>
          <Select
            labelId="property-type"
            id="property-type"
            value={propertyType}
            label="House Type"
            onChange={(event) => setPropertyType(event.target.value)}
          >
            {Object.keys(propertyTypesDict).map((type) => {
              return (
                <MenuItem key={type} value={type}>{type}</MenuItem>
              )
            })}
          </Select>
        </FormControl>
        <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
          <InputLabel id="bedrooms">Beds</InputLabel>
          <Select
            labelId="bedrooms"
            id="bedrooms"
            value={beds}
            label="Beds"
            onChange={(event) => {
              console.log(event.target.value)
              setBeds(event.target.value)
            }}
          >
            {propertyTypesDict[propertyType] && propertyTypesDict[propertyType].map((bed) => {
              return (
                <MenuItem key={bed} value={bed}>{bed}</MenuItem>
              )
            })}
          </Select>
        </FormControl>
      </Box>
      {filteredTransactions.length > 0 ? (
        <RecentTransactionTable transactions={filteredTransactions} />
      ) : (
        <Typography>No transactions found</Typography>
      )}
    </Box>
  );
}

export default RecentTransactions;