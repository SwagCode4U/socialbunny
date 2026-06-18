import { useState } from "react";
import { motion } from "framer-motion";

const interests = [
  { value: "React", emoji: "⚛️" },
  { value: "Python", emoji: "🐍" },
  { value: "FastAPI", emoji: "⚡" },
  { value: "JavaScript", emoji: "📜" },
  { value: "UI/UX", emoji: "🎨" },
  { value: "Other", emoji: "🚀" },
];

export default function WizardForm({ referredById, onComplete }) {
  const [form, setForm] = useState({ name: "", phone: "", interest: "" });
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    const token = localStorage.getItem("access_token");
    try {
      const res = await fetch("http://127.0.0.1:8000/api/auth/wizard", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name: form.name,
          phone: form.phone,
          interest: form.interest,
          referred_by_id: referredById || null,
        }),
      });

      if (!res.ok) throw new Error("Wizard failed");

      const user = await res.json();
      onComplete(user);
    } catch (err) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="space-y-5"
    >
      <div className="text-center mb-4">
        <motion.div
          className="text-3xl mb-2"
          animate={{ rotate: [0, -5, 5, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          ✨
        </motion.div>
        <h2 className="text-lg font-semibold text-gray-800">
          Almost there!
        </h2>
        <p className="text-gray-400 text-sm">
          Just a few more details to get started
        </p>
      </div>

      <div>
        <label className="block text-xs font-medium text-gray-500 mb-1.5 uppercase tracking-wider">
          Full Name
        </label>
        <motion.input
          whileFocus={{ scale: 1.01 }}
          className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-400/50 focus:border-indigo-400 transition-all"
          placeholder="e.g. John Doe"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />
      </div>

      <div>
        <label className="block text-xs font-medium text-gray-500 mb-1.5 uppercase tracking-wider">
          Phone Number
        </label>
        <motion.input
          whileFocus={{ scale: 1.01 }}
          className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-400/50 focus:border-indigo-400 transition-all"
          placeholder="e.g. 9876543210"
          value={form.phone}
          onChange={(e) => setForm({ ...form, phone: e.target.value })}
          required
        />
      </div>

      <div>
        <label className="block text-xs font-medium text-gray-500 mb-1.5 uppercase tracking-wider">
          What interests you?
        </label>
        <div className="grid grid-cols-2 gap-2">
          {interests.map(({ value, emoji }) => (
            <motion.button
              key={value}
              type="button"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setForm({ ...form, interest: value })}
              className={`px-3 py-3 rounded-xl text-sm font-medium transition-all border ${
                form.interest === value
                  ? "bg-indigo-50 border-indigo-400 text-indigo-700 shadow-sm shadow-indigo-200"
                  : "bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300"
              }`}
            >
              <span className="mr-1.5">{emoji}</span>
              {value}
            </motion.button>
          ))}
        </div>
      </div>

      <motion.button
        type="submit"
        disabled={submitting || !form.interest}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-xl font-semibold shadow-lg shadow-indigo-200 hover:shadow-xl hover:shadow-indigo-300 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {submitting ? (
          <span className="flex items-center justify-center gap-2">
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            Saving...
          </span>
        ) : (
          "Get Started 🚀"
        )}
      </motion.button>
    </motion.form>
  );
}
