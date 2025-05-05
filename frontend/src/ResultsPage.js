import React, { useEffect, useState } from "react";

const ResultsPage = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const searchTerm = localStorage.getItem("searchTerm") || "";
    fetch(`http://localhost:5000/show_result?searchTerm=${encodeURIComponent(searchTerm)}`)
      .then((res) => res.json())
      .then((data) => {
        setProducts(data);
      })
      .catch((err) => console.error("Error loading data:", err));
  }, []);

  const handleBack = () => {
    window.location.href = "/";
  };

  return (
    <div className="results-container">
      {/* ✅ Back button */}
      <button className="back-button" onClick={handleBack}>
        ⬅ 
      </button>

      <h1 className="results-title">Top Results</h1>
      <div className="grid">
        {products.map((item, index) => (
          <div className="product-card" key={index}>
            <h2>{item.title}</h2>
            <p className="price">{item.price}</p>
            <p className="seller">{item.seller}</p>
            {item.link ? (
              <a href={item.link} target="_blank" rel="noopener noreferrer">
                <button className="buy-btn">View Product</button>
              </a>
            ) : (
              <button className="buy-btn disabled">No Link</button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResultsPage;
