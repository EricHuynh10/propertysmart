import * as React from 'react';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import NearbySummaryTable from './NearbySummaryTable';
import RecentTransactions from './RecentTransactions';
import { Typography } from '@mui/material';

function CustomTabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box>
          {children}
        </Box>
      )}
    </div>
  );
}

CustomTabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

export default function BasicTabs({ nearbySummary, transactions }) {
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={value} onChange={handleChange}>
          <Tab label="Summary" id='tab-0' sx={{ paddingBottom: 0, fontWeight: 'bold' }}/>
          <Tab label="Transactions" id='tab-1' sx={{ paddingBottom: 0, fontWeight: 'bold' }}/>
        </Tabs>
      </Box>
      <CustomTabPanel value={value} index={0}>
        <NearbySummaryTable nearbySummary={nearbySummary} />
      </CustomTabPanel>
      <CustomTabPanel value={value} index={1}>
        <RecentTransactions transactions={transactions} />
      </CustomTabPanel>
    </Box>
  );
}
