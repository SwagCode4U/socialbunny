import { Routes, Route } from 'react-router-dom'
import { ThemeProvider } from '@emotion/react'
import Navbar from './components/Navbar.jsx'
import Footer from './components/Footer.jsx'
import useLenis from './hooks/useLenis.js'
import theme from './styles/theme.js'
import AdminLogin from './pages/AdminLogin.jsx'
import AdminDashboard from './pages/AdminDashboard.jsx'
import Register from './pages/Register.jsx'
import './index.css'

function Home() {
  return (
    <div className="container">
      <h1 className="text-4xl font-bold text-center bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
        SocialBunny
      </h1>
      <p className="text-center text-gray-600 mt-2">
        Learn FastAPI + React through hands-on projects
      </p>
    </div>
  )
}

function App() {
  useLenis()

  return (
    <ThemeProvider theme={theme}>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </main>
      <Footer />
    </ThemeProvider>
  )
}

export default App
