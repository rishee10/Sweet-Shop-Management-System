import { useEffect, useState, useRef } from "react";
import api from "../api/axios";
import Navbar from "../components/Navbar";
import HeroBanner from "../components/HeroBanner";

export default function AdminDashboard() {
  const [sweets, setSweets] = useState([]);
  const [editingId, setEditingId] = useState(null);

  const formRef = useRef(null); // ✅ ref for auto scroll

  const [form, setForm] = useState({
    name: "",
    category: "",
    price: "",
    quantity: "",
    image: null,
  });

  const loadSweets = async () => {
    const res = await api.get("sweets/");
    setSweets(res.data);
  };

  useEffect(() => {
    loadSweets();
  }, []);

  // ✅ SAME LOGIC — NOT TOUCHED
  const submitSweet = async () => {
    try {
      const formData = new FormData();
      formData.append("name", form.name);
      formData.append("category", form.category);
      formData.append("price", form.price);
      formData.append("quantity", form.quantity);

      if (form.image) {
        formData.append("image", form.image);
      }

      if (editingId) {
        await api.put(`admin/sweets/${editingId}/`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        alert("Sweet updated successfully");
      } else {
        await api.post("admin/sweets/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        alert("Sweet added successfully");
      }

      setForm({
        name: "",
        category: "",
        price: "",
        quantity: "",
        image: null,
      });
      setEditingId(null);
      loadSweets();
    } catch (err) {
      console.error(err.response?.data);
      alert("Admin action failed");
    }
  };

  // ✅ EDIT + AUTO SCROLL
  const editSweet = (s) => {
    setEditingId(s.id);
    setForm({
      name: s.name,
      category: s.category,
      price: s.price,
      quantity: s.quantity,
      image: null,
    });

    // 🔥 Smooth auto scroll to form
    setTimeout(() => {
      formRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }, 100);
  };

  const deleteSweet = async (id) => {
    if (!window.confirm("Are you sure?")) return;
    await api.delete(`admin/sweets/${id}/delete/`);
    loadSweets();
  };

  return (
    <>
      <HeroBanner />
      <Navbar />

      <div className="dashboard">
        <h2 className="dashboard-title">🧁 Sweet Shop Admin Panel</h2>

        {/* FORM CARD */}
        <div
          ref={formRef}
          className={`card admin-form-card ${
            editingId ? "edit-highlight" : ""
          }`}
        >
          <h3>{editingId ? "Edit Sweet" : "Add New Sweet"}</h3>

          <div className="form-grid">
            <input
              className="input"
              placeholder="Sweet Name"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />

            <input
              className="input"
              placeholder="Category"
              value={form.category}
              onChange={(e) => setForm({ ...form, category: e.target.value })}
            />

            <input
              className="input"
              type="number"
              placeholder="Price"
              value={form.price}
              onChange={(e) => setForm({ ...form, price: e.target.value })}
            />

            <input
              className="input"
              type="number"
              placeholder="Quantity"
              value={form.quantity}
              onChange={(e) => setForm({ ...form, quantity: e.target.value })}
            />

            <input
              className="input"
              type="file"
              accept="image/*"
              onChange={(e) =>
                setForm({ ...form, image: e.target.files[0] })
              }
            />
          </div>

          <button className="button full-width" onClick={submitSweet}>
            {editingId ? "Update Sweet" : "Add Sweet"}
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
                <h4>{s.name}</h4>
                <p>{s.category}</p>
                <p>₹{s.price}</p>
                <p>Qty: {s.quantity}</p>

                <div className="admin-btn-group">
                  <button
                    className="buy-btn"
                    onClick={() => editSweet(s)}
                  >
                    Edit
                  </button>

                  <button
                    className="buy-btn delete-btn"
                    onClick={() => deleteSweet(s.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* LOGOUT SECTION */}
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
