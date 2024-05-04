import React from 'react';
import './App.css';

const Pagination = ({ currentPage, totalRecords, onPageChange }) => {
  const recordsPerPage = 10;
  const pageLimit = 5;
    const totalPages = totalRecords === 0 ? 1 : Math.ceil(totalRecords / recordsPerPage);

  const getPaginationGroup = () => {
    let start = Math.floor((currentPage - 1) / pageLimit) * pageLimit;
    return new Array(Math.min(pageLimit, totalPages - start)).fill().map((_, idx) => start + idx + 1);
  };

  const handlePageClick = (page) => {
    onPageChange(page);
  };

  const handleNextClick = () => {
    onPageChange((prevPage) => Math.min(prevPage + 1, totalPages));
  };

  const handlePrevClick = () => {
    onPageChange((prevPage) => Math.max(prevPage - 1, 1));
  };

  return (
    <div className="pagination" >
      <button onClick={handlePrevClick} disabled={currentPage === 1}>
        Prev
      </button>
      {getPaginationGroup().map((item, index) => (
        <button
          key={index}
          onClick={() => handlePageClick(item)}
          disabled={currentPage === item}
          style={{ fontWeight: currentPage === item ? 'bold' : 'normal' }}
        >
          {item}
        </button>
      ))}
      <button onClick={handleNextClick} disabled={currentPage === totalPages}>
        Next
      </button>
    </div>
  );
};

export default Pagination;
