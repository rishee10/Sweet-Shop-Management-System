import { useEffect, useState } from "react";
import api from "../api/axios";
import Navbar from "../components/Navbar";
import HeroBanner from "../components/HeroBanner";

export default function UserDashboard() {
  const [sweets, setSweets] = useState([]);

  const [filters, setFilters] = useState({
    name: "",
    category: "",
    min_price: "",
    max_price: "",
  });

  const loadSweets = async () => {
    const params = new URLSearchParams();

    if (filters.name) params.append("name", filters.name);
    if (filters.category) params.append("category", filters.category);
    if (filters.min_price) params.append("min_price", filters.min_price);
    if (filters.max_price) params.append("max_price", filters.max_price);

    const url =
      params.toString().length > 0
        ? `sweets/search/?${params.toString()}`
        : "sweets/";

    const res = await api.get(url);
    setSweets(res.data);
  };

  useEffect(() => {
    loadSweets();
  }, []);

  const purchaseSweet = async (id) => {
    try {
      await api.post(`sweets/${id}/purchase/`);
      loadSweets();
    } catch {
      alert("Out of stock");
    }
  };

  return (
    <>
      <HeroBanner />
      <Navbar />

      <div className="dashboard">
        <h2>🍭 Explore Our Sweets</h2>

        {/* SEARCH FILTERS */}
        <div className="card">
          <h3>Search Sweets</h3>

          <input
            className="input"
            placeholder="Sweet Name"
            value={filters.name}
            onChange={(e) =>
              setFilters({ ...filters, name: e.target.value })
            }
          />

          <input
            className="input"
            placeholder="Category"
            value={filters.category}
            onChange={(e) =>
              setFilters({ ...filters, category: e.target.value })
            }
          />

          <input
            className="input"
            type="number"
            placeholder="Min Price"
            value={filters.min_price}
            onChange={(e) =>
              setFilters({ ...filters, min_price: e.target.value })
            }
          />

          <input
            className="input"
            type="number"
            placeholder="Max Price"
            value={filters.max_price}
            onChange={(e) =>
              setFilters({ ...filters, max_price: e.target.value })
            }
          />

          <button className="button" onClick={loadSweets}>
            Apply Filters
          </button>
        </div>

        {/* SWEETS GRID */}
        <div className="sweets-grid">
          {sweets.map((s) => (
            <div className="product-card" key={s.id}>
              {s.image && (
                <img
                  src={`http://127.0.0.1:8000${s.image}`}
                  alt={s.name}
                />
              )}

              <div className="product-content">
                <span className="product-badge">
                  {s.quantity > 5 ? "🔥 Trending" : "👍 Recommended"}
                </span>

                <div className="product-name">{s.name}</div>

                <div className="product-category">
                   {s.category}
                </div>

                <div className="product-price">
                  ₹{s.price}
                </div>

                <div className="product-qty">
                  {s.quantity > 0
                    ? `📦 ${s.quantity} available`
                    : "❌ Out of stock"}
                </div>

                <button
                  className="buy-btn"
                  disabled={s.quantity === 0}
                  onClick={() => purchaseSweet(s.id)}
                >
                  {s.quantity === 0 ? "Sold Out" : "Buy Now"}
                </button>
              </div>
            </div>
          ))}
        </div>

        {sweets.length === 0 && <p>No sweets found</p>}

        <div className="logout-section">
  <button
    className="button"
    style={{ width: "160px" }}
    onClick={() => {
      localStorage.clear();
      window.location.href = "/";
    }}
  >
    Logout
  </button>
</div>

      </div>
    </>
  );
}
