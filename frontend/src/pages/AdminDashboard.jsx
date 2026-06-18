import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import FriendsList from "../components/FriendsList.jsx";

export default function AdminDashboard() {
  const [admin, setAdmin] = useState(null);
  const [copied, setCopied] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("admin_token");
    if (!token) {
      navigate("/admin/login");
      return;
    }

    fetch("http://127.0.0.1:8000/api/admin/me", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then(setAdmin)
      .catch(() => {
        localStorage.removeItem("admin_token");
        navigate("/admin/login");
      });
  }, [navigate]);

  const copyLink = () => {
    navigator.clipboard.writeText(admin.referral_link);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleLogout = () => {
    localStorage.removeItem("admin_token");
    navigate("/admin/login");
  };

  if (!admin) return <p className="container text-center">Loading...</p>;

  return (
    <div className="container">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">
          Welcome, {admin.name}!
        </h1>
        <button
          onClick={handleLogout}
          className="text-sm text-red-500 hover:text-red-700"
        >
          Logout
        </button>
      </div>

      <div className="card border border-indigo-100">
        <h2 className="text-lg font-semibold mb-2">Your Referral Link</h2>
        <div className="flex gap-2">
          <input
            className="flex-1 px-3 py-2 border rounded-lg bg-gray-50 text-sm"
            value={admin.referral_link}
            readOnly
          />
          <button
            onClick={copyLink}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm"
          >
            {copied ? "Copied!" : "Copy"}
          </button>
        </div>
        <p className="mt-2 text-sm text-gray-500">
          Friends referred: <strong>{admin.referral_count}</strong>
        </p>
      </div>

      <FriendsList adminId={admin.id} />
    </div>
  );
}
