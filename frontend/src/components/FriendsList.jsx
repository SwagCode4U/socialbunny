import { useState, useEffect } from "react";

export default function FriendsList({ adminId }) {
  const [friends, setFriends] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("admin_token");
    if (!token) {
      setLoading(false);
      return;
    }

    fetch(`http://127.0.0.1:8000/api/admin/${adminId}/friends`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => setFriends(data.friends || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [adminId]);

  if (loading) return <p className="text-gray-500">Loading friends...</p>;

  return (
    <div className="mt-6">
      <h3 className="text-xl font-semibold mb-3">
        My Friends ({friends.length})
      </h3>

      {friends.length === 0 ? (
        <p className="text-gray-500">
          No friends yet. Share your referral link!
        </p>
      ) : (
        <ul className="space-y-2">
          {friends.map((f) => (
            <li
              key={f.id}
              className="p-3 bg-gray-50 rounded-lg flex justify-between items-center"
            >
              <div>
                <span className="font-medium">{f.name}</span>
                <span className="text-gray-500 ml-2 text-sm">{f.email}</span>
              </div>
              <span className="text-xs text-gray-400">
                {new Date(f.created_at).toLocaleDateString()}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
