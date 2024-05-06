import React, { useState  } from 'react';
// import Pagination from './Pagination';
import AppStyles from './App.module.css';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import TopSuburbsByYield from './components/TopSuburbsByYield';

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className={AppStyles.App}>
      <Header />
      <SearchBar setResult={setResult} />
      <TopSuburbsByYield />
    </div>
    // <div className="App">

      
    //   <div class="main">
    //     {submitOption && (
    //     <h2>
    //       {submitOption.value.suburb.toUpperCase()}, {submitOption.value.state.toUpperCase()}, {submitOption.value.postcode}
    //     </h2>
    //     )}

    //     {result && result.properties && (
    //     <div class="table-container suburb-info">
    //       <table className="table">
    //         <caption>
    //           Median Price and Yield
    //         </caption>
    //         <thead>
    //         <tr>
    //           <th style={{ width: '8%' }}>House Type</th>
    //           <th style={{ width: '3%' }}>Beds</th>
    //           <th style={{ width: '10%' }}>Median Price ($)</th>
    //           <th style={{ width: '10%' }}>Annual Growth (%)</th>
    //           <th style={{ width: '8%' }}>Last 12M Sold</th>
    //           <th style={{ width: '9%' }}>Rental Yield (%)</th>
    //           <th style={{ width: '8%' }}>Total Yield (%)</th>
    //         </tr>
    //         </thead>
    //         <tbody>
    //           {result.properties.map((item, index) => (
    //             <tr key={index}>
    //                 <td style={{ width: '8%' }}>{item.propertyType}</td>
    //                 <td style={{ width: '3%' }}>{item.beds}</td>
    //                 <td style={{ width: '10%' }}>{item.medianPrice ? item.medianPrice.toLocaleString() : '-'}</td>
    //                 <td style={{ width: '10%' }}>{item.annualGrowth ? `${(item.annualGrowth * 100).toFixed(1)}%` : '-'}</td>
    //                 <td style={{ width: '8%' }}>{item.soldThisYear ? item.soldThisYear.toLocaleString() : '-'}</td>
    //                 <td style={{ width: '9%' }}>{item.rentalYield ? `${(item.rentalYield * 100).toFixed(1)}%` : '-'}</td>
    //                 <td style={{ width: '8%' }}>{item.totalYield ? `${(item.totalYield * 100).toFixed(1)}%` : '-'}</td>
    //             </tr>
    //           ))}
    //         </tbody>
    //       </table>
    //     </div>
    //     )}

    //     {result && result.schools && (
    //     <div class="table-container suburb-info">
    //       <table className='table'>
    //         <caption>
    //           Nearby Schools
    //         </caption>
    //         <thead>
    //           <tr>
    //             <th style={{ width: '15%' }}>School</th>
    //             <th style={{ width: '5%' }}>School Type</th>
    //             <th style={{ width: '5%' }}>Education Level</th>
    //             <th style={{ width: '5%' }}>Score</th>
    //           </tr>
    //         </thead>
    //         <tbody>
    //           {result.schools.map((school, index) => (
    //             <tr key={index}>
    //               <td style={{ width: '15%', textAlign: 'left' }}>{school.school}</td>
    //               <td style={{ width: '5%' }}>{school.schoolType}</td>
    //               <td style={{ width: '5%' }}>{school.educationLevel}</td>
    //               <td style={{ width: '5%' }}>{school.score ? school.score : '-'}</td>
    //             </tr>
    //           ))}
    //         </tbody>
    //       </table>
    //     </div>
    //     )}

    //     
    // </div>
  )
};

export default App;
