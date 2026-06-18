import { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { motion, AnimatePresence } from "framer-motion";
import WizardForm from "../components/WizardForm.jsx";

const FloatingShape = ({ color, size, x, y, delay, duration }) => (
  <motion.div
    className="absolute rounded-full blur-3xl opacity-20"
    style={{
      width: size,
      height: size,
      background: color,
      left: x,
      top: y,
    }}
    animate={{
      y: [0, -30, 0],
      x: [0, 15, 0],
    }}
    transition={{
      duration,
      repeat: Infinity,
      delay,
      ease: "easeInOut",
    }}
  />
);

const Particle = ({ x, delay }) => (
  <motion.div
    className="absolute w-1 h-1 bg-white/40 rounded-full"
    style={{ left: x, bottom: 0 }}
    animate={{
      y: [0, -400],
      opacity: [0, 1, 0],
    }}
    transition={{
      duration: 4 + Math.random() * 3,
      repeat: Infinity,
      delay,
      ease: "linear",
    }}
  />
);

function ReferralCodeSection({ refCode, referrer, refLoading }) {
  return (
    <AnimatePresence mode="wait">
      {refLoading ? (
        <motion.div
          key="loading"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="h-12 flex items-center justify-center"
        >
          <div className="w-5 h-5 border-2 border-indigo-400 border-t-transparent rounded-full animate-spin" />
        </motion.div>
      ) : refCode && referrer ? (
        <motion.div
          key="success"
          initial={{ opacity: 0, y: -10, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -10 }}
          className="bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200/60 rounded-2xl p-4 mb-6 text-center shadow-sm"
        >
          <motion.span
            className="text-3xl inline-block"
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            🎉
          </motion.span>
          <p className="text-emerald-800 font-medium mt-1">
            You were invited by{" "}
            <span className="font-bold text-emerald-600">{referrer.name}</span>
          </p>
          <p className="text-emerald-600/60 text-xs mt-0.5">
            Code: <span className="font-mono font-semibold">{refCode}</span>
          </p>
        </motion.div>
      ) : refCode && !referrer ? (
        <motion.div
          key="error"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0 }}
          className="bg-red-50 border border-red-200 rounded-2xl p-4 mb-6 text-center"
        >
          <p className="text-red-600 text-sm font-medium">
            Invalid referral link
          </p>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}

function GoogleButtonSection({ onSuccess, onError, error }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.3 }}
      className="flex flex-col items-center gap-5"
    >
      <div className="text-center">
        <p className="text-gray-500 text-sm font-medium uppercase tracking-wider">
          Sign in with
        </p>
      </div>

      <motion.div
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.97 }}
        className="rounded-2xl shadow-lg shadow-indigo-200/50 overflow-hidden border border-gray-100"
      >
        <GoogleLogin
          onSuccess={onSuccess}
          onError={() => onError("Google sign-in failed")}
          theme="outline"
          size="large"
          text="signin_with"
          shape="rectangular"
          width="320"
        />
      </motion.div>

      <AnimatePresence>
        {error && (
          <motion.p
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="text-red-500 text-sm text-center bg-red-50 px-4 py-2 rounded-xl"
          >
            {error}
          </motion.p>
        )}
      </AnimatePresence>

      <p className="text-gray-400 text-xs text-center max-w-xs leading-relaxed">
        By signing in, you agree to our terms. We only use your email and
        profile info to create your account.
      </p>
    </motion.div>
  );
}

function WelcomeRedirect() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ type: "spring", stiffness: 200, damping: 15 }}
      className="text-center py-12"
    >
      <motion.div
        animate={{ rotate: [0, 10, -10, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
        className="text-6xl mb-4"
      >
        🐰
      </motion.div>
      <p className="text-emerald-600 text-xl font-semibold">
        Welcome aboard!
      </p>
      <p className="text-emerald-500/60 text-sm mt-1">
        Redirecting to your dashboard...
      </p>
      <motion.div
        animate={{ width: ["0%", "100%"] }}
        transition={{ duration: 1.5, ease: "easeInOut" }}
        className="h-1 bg-gradient-to-r from-emerald-400 to-emerald-600 rounded-full mt-4 mx-auto max-w-xs"
      />
    </motion.div>
  );
}

export default function Register() {
  const [searchParams] = useSearchParams();
  const [referrer, setReferrer] = useState(null);
  const [refLoading, setRefLoading] = useState(true);
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const refCode = searchParams.get("ref");

  useEffect(() => {
    if (refCode) {
      fetch(`http://127.0.0.1:8000/api/referral/lookup/${refCode}`)
        .then((r) => {
          if (!r.ok) throw new Error("Invalid code");
          return r.json();
        })
        .then(setReferrer)
        .catch(() => setReferrer(null))
        .finally(() => setRefLoading(false));
    } else {
      setRefLoading(false);
    }
  }, [refCode]);

  const handleGoogleSuccess = async (credentialResponse) => {
    setError("");
    try {
      const res = await fetch("http://127.0.0.1:8000/api/auth/google", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_token: credentialResponse.credential }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Google login failed");
      }

      const data = await res.json();
      localStorage.setItem("access_token", data.access_token);
      setUser(data.user);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleWizardComplete = (updatedUser) => {
    setUser(updatedUser);
    setTimeout(() => navigate("/dashboard"), 1500);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500" />

      {/* Floating shapes */}
      <FloatingShape color="#818cf8" size={300} x="-5%" y="-10%" delay={0} duration={6} />
      <FloatingShape color="#c084fc" size={200} x="80%" y="60%" delay={1} duration={7} />
      <FloatingShape color="#f472b6" size={250} x="70%" y="-5%" delay={2} duration={8} />
      <FloatingShape color="#60a5fa" size={180} x="-8%" y="70%" delay={0.5} duration={6.5} />

      {/* Particles */}
      {[...Array(12)].map((_, i) => (
        <Particle key={i} x={`${5 + i * 8}%`} delay={i * 0.4} />
      ))}

      {/* Main Card */}
      <motion.div
        initial={{ opacity: 0, y: 40, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="relative w-full max-w-md"
      >
        {/* Glass card */}
        <div className="bg-white/90 backdrop-blur-xl rounded-3xl shadow-2xl shadow-indigo-900/20 p-8 border border-white/50">
          {/* Logo + Title */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.15 }}
            className="text-center mb-8"
          >
            <motion.div
              className="text-5xl mb-3"
              animate={{ y: [0, -5, 0] }}
              transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
            >
              🐰
            </motion.div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Join SocialBunny
            </h1>
            <p className="text-gray-500 text-sm mt-1">
              Your learning community awaits
            </p>
          </motion.div>

          {/* Referral section */}
          <ReferralCodeSection
            refCode={refCode}
            referrer={referrer}
            refLoading={refLoading}
          />

          {/* Main content */}
          <AnimatePresence mode="wait">
            {!user ? (
              <motion.div key="google" exit={{ opacity: 0, y: -20 }}>
                <GoogleButtonSection
                  onSuccess={handleGoogleSuccess}
                  onError={setError}
                  error={error}
                />
              </motion.div>
            ) : !user.is_onboarded ? (
              <motion.div
                key="wizard"
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -30 }}
              >
                <WizardForm
                  referredById={referrer ? referrer.id : null}
                  onComplete={handleWizardComplete}
                />
              </motion.div>
            ) : (
              <motion.div key="welcome">
                <WelcomeRedirect />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </div>
  );
}
