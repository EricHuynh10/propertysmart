import React, { useState, useEffect  } from 'react';
import Select from 'react-select';
import axios from 'axios';
import './App.css';
import Pagination from './Pagination'; 


function App() {
  const [inputValue, setInputValue] = useState('');
  const [selectedOption, setSelectedOption] = useState(null);
  const [result, setResult] = useState(null);
  const [locationOptions, setLocationOptions] = useState([]);
  const [submitOption, setSubmitOption] = useState(null);
  const [top10, setTop10] = useState(null);
  const [stateValue, setStateValue] = useState('all');
  const [yieldValue, setYieldValue] = useState('rentalYield');
  const [propertyTypeValue, setPropertyTypeValue] = useState('all');
  const [remoteness, setRemotenessValue] = useState('0');
  const [totalRecords, setTotalRecords] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);


  useEffect(() => {
    fetchLocationOptions();
  }, []);

  useEffect(() => {
    fetchTop10();
  }, [stateValue, yieldValue, propertyTypeValue, remoteness, currentPage]);

  useEffect(() => {
    fetchTotalRecords();
  }, [stateValue, yieldValue, propertyTypeValue]);

  const fetchLocationOptions = async (inputValue) => {
    try {
      let url = `${process.env.REACT_APP_BACKEND_URL}/location-options`;
      if (inputValue && inputValue !== '') {
        url += `?search=${inputValue}`;
      }
      const response = await axios.get(url);
      let options = []; // Declare options as an empty array
      options = response.data.map((location) => ({
        label: `${location.suburb}, ${location.state}, ${location.postcode}`,
        value: {
          suburb: location.suburb,
          state: location.state,
          postcode: location.postcode
        }
      }));
      setLocationOptions(options);
      return options;
    } catch (error) {
      console.error('Error fetching location options: ', error);
    }
  };

  const fetchTop10 = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/top10?state=${stateValue}&sortBy=${yieldValue}&propertyType=${propertyTypeValue}&remoteness=${remoteness}&page=${currentPage}`);
      setTop10(response.data);
    } catch (error) {
      console.error('Error fetching top 10: ', error);
    }
  };

  const fetchTotalRecords = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/total-records?state=${stateValue}&sortBy=${yieldValue}&propertyType=${propertyTypeValue}&remoteness=${remoteness}`);
      setTotalRecords(response.data.totalRecords);
    } catch (error) {
      console.error('Error fetching total records: ', error);
    }
  };

  const handleStateChange = (event) => {
    setStateValue(event.target.value);
  };

  const yieldTypeChange = (event) => {
    setYieldValue(event.target.value);
  };

  const handlePropertyTypeChange = (event) => {
    setPropertyTypeValue(event.target.value);
  };

  const handleRemotenessChange = (event) => {
    setRemotenessValue(event.target.value);
  };

  const handleInputChange = (newValue) => {
    setInputValue(newValue);
    fetchLocationOptions(newValue);
    return newValue;
  };

  const handleChange = (option) => {
    setSelectedOption(option);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setSubmitOption(selectedOption);
      const selectedOptionString = selectedOption.value.suburb + '-' + selectedOption.value.state + '-' + selectedOption.value.postcode;
      const selectedOptionStringFormatted = selectedOptionString.replace(/\s+/g, '-').toLowerCase();
      const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/suburb/${selectedOptionStringFormatted}`);
      setResult(response.data);
    } catch (error) {
      console.error('Error fetching data: ', error);
    }
  };

  const onPageChange = (page) => {
    setCurrentPage(page);
  };


  return (
    <div style={{ display: 'flex', alignItems: 'center', height: '100vh', flexDirection: 'column', textAlign: 'center' }}>
      <h1>Real Estate Review</h1>
      <div style={{ width: '60%' }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', width: '100%', textAlign: 'left' }}>
          <Select
            name="suburb"
            inputValue={inputValue}
            onInputChange={handleInputChange}
            onChange={handleChange}
            options={locationOptions}
            placeholder="Enter a suburb, state, postcode"
            styles={{ container: (base) => ({ ...base, flex: 1 }) }}  // Make Select flex in size
          />
          <button type="submit" style={{ marginLeft: '0.5rem' }}>Search</button>
        </form>

        {submitOption && (
        <h2 style={{ textAlign: 'left', fontWeight: 'bold' }}>
          {submitOption.value.suburb.toUpperCase()}, {submitOption.value.state.toUpperCase()}, {submitOption.value.postcode}
        </h2>
        )}

        {result && result.properties && (
          <div style={{ width: '82%' }}>
            <table className="table">
              <caption style={{ textAlign: 'left', fontWeight: 'bold', marginBottom: '0.2rem' }}>
                Median Price and Yield
              </caption>
              <thead>
              <tr>
                <th style={{ width: '8%' }}>House Type</th>
                <th style={{ width: '3%' }}>Beds</th>
                <th style={{ width: '10%' }}>Median Price ($)</th>
                <th style={{ width: '10%' }}>Annual Growth (%)</th>
                <th style={{ width: '8%' }}>Last 12M Sold</th>
                <th style={{ width: '9%' }}>Rental Yield (%)</th>
                <th style={{ width: '8%' }}>Total Yield (%)</th>
              </tr>
              </thead>
              <tbody>
                {result.properties.map((item, index) => (
                  <tr key={index}>
                      <td style={{ width: '8%' }}>{item.propertyType}</td>
                      <td style={{ width: '3%' }}>{item.beds}</td>
                      <td style={{ width: '10%' }}>{item.medianPrice ? item.medianPrice.toLocaleString() : '-'}</td>
                      <td style={{ width: '10%' }}>{item.annualGrowth ? `${(item.annualGrowth * 100).toFixed(1)}%` : '-'}</td>
                      <td style={{ width: '8%' }}>{item.soldThisYear ? item.soldThisYear.toLocaleString() : '-'}</td>
                      <td style={{ width: '9%' }}>{item.rentalYield ? `${(item.rentalYield * 100).toFixed(1)}%` : '-'}</td>
                      <td style={{ width: '8%' }}>{item.totalYield ? `${(item.totalYield * 100).toFixed(1)}%` : '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {result && result.schools && (
          <div style={{ width: '82%' }}>
            <table className='table'>
              <caption style={{ textAlign: 'left', fontWeight: 'bold', marginBottom: '0.2rem', marginTop: '1rem' }}>
                Nearby Schools
              </caption>
              <thead>
                <tr>
                  <th style={{ width: '15%' }}>School</th>
                  <th style={{ width: '5%' }}>School Type</th>
                  <th style={{ width: '5%' }}>Education Level</th>
                  <th style={{ width: '5%' }}>Score</th>
                </tr>
              </thead>
              <tbody>
                {result.schools.map((school, index) => (
                  <tr key={index}>
                    <td style={{ width: '15%', textAlign: 'left' }}>{school.school}</td>
                    <td style={{ width: '5%' }}>{school.schoolType}</td>
                    <td style={{ width: '5%' }}>{school.educationLevel}</td>
                    <td style={{ width: '5%' }}>{school.score ? school.score : '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <h2 style={{ textAlign: 'left', fontWeight: 'bold' }}>Top 10 Investments by Yield</h2>
        {top10 && (
        <div>
          <div style={{ textAlign: 'left', marginBottom: '1rem' }}>
            <label>Filter by: </label>
            <select onChange={handleStateChange}>
              <option value="all">All States</option>
              <option value="act">ACT</option>
              <option value="nsw">NSW</option>
              <option value="nt">NT</option>
              <option value="qld">QLD</option>
              <option value="sa">SA</option>
              <option value="tas">TAS</option>
              <option value="vic">VIC</option>
              <option value="wa">WA</option>
            </select>
            <select onChange={yieldTypeChange}>
              <option value="rentalYield">Rental Yield</option>
              <option value="annualGrowth">Price Growth</option>
              <option value="totalYield">Total Yield</option>
            </select>
            <select onChange={handlePropertyTypeChange}>
              <option value="all">All House Types</option>
              <option value="house">House</option>
              <option value="unit">Apartment</option>
            </select>
            <select onChange={handleRemotenessChange}>
              <option value="0">Major Cities of Australia</option>
              <option value="1">Inner Regional Australia</option>
              <option value="2">Outer Regional Australia</option>
              <option value="3">Remote Australia</option>
              <option value="4">Very Remote Australia</option>
              <option value="all">All Regions</option>
            </select>
          </div>
          <table className="table">
            <thead>
            <tr>
              <th style={{ width: '10%' }}>Suburb</th>
              <th style={{ width: '3%' }}>State</th>
              <th style={{ width: '5%' }}>Postcode</th>
              <th style={{ width: '8%' }}>House Type</th>
              <th style={{ width: '3%' }}>Beds</th>
              <th style={{ width: '10%' }}>Median Price ($)</th>
              <th style={{ width: '10%' }}>Annual Growth (%)</th>
              <th style={{ width: '8%' }}>Last 12M Sold</th>
              <th style={{ width: '9%' }}>Rental Yield (%)</th>
              <th style={{ width: '8%' }}>Total Yield (%)</th>
            </tr>
            </thead>
            <tbody>
              {top10.map((item, index) => (
                <tr key={index}>
                  <td style={{ width: '10%', textAlign: 'left' }}>{item.suburb}</td>
                  <td style={{ width: '3%' }}>{item.state}</td>
                  <td style={{ width: '5%' }}>{item.postcode}</td>
                  <td style={{ width: '8%' }}>{item.propertyType}</td>
                  <td style={{ width: '3%' }}>{item.beds}</td>
                  <td style={{ width: '10%' }}>{item.medianPrice ? item.medianPrice.toLocaleString() : '-'}</td>
                  <td style={{ width: '10%' }}>{item.annualGrowth ? `${(item.annualGrowth * 100).toFixed(1)}%` : '-'}</td>
                  <td style={{ width: '8%' }}>{item.soldThisYear ? item.soldThisYear.toLocaleString() : '-'}</td>
                  <td style={{ width: '9%' }}>{item.rentalYield ? `${(item.rentalYield * 100).toFixed(1)}%` : '-'}</td>
                  <td style={{ width: '8%' }}>{item.totalYield ? `${(item.totalYield * 100).toFixed(1)}%` : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        )}
      </div>
      <Pagination totalRecords={totalRecords} 
                  onPageChange={onPageChange}
                  currentPage={currentPage} />
    </div>
  )
};

export default App;
