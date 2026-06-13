import { useState, useEffect } from 'react'
import { ThemeProvider } from '@emotion/react'
import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import Footer from './components/Footer.jsx'
import useLenis from './hooks/useLenis.js'
import theme from './styles/theme.js'
import './index.css'

function App() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)
  useLenis()

  useEffect(() => {
    // Example API call - update with your backend URL
    fetch('http://localhost:8000/')
      .then(res => res.json())
      .then(data => {
        setMessage(data.message)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error:', err)
        setLoading(false)
      })
  }, [])

  return (
    <ThemeProvider theme={theme}>
      <Navbar />
      <main className="container">
        <Hero title="SocialBunny" subtitle="Making Social App By Hani" />
        <div className="card">
          {loading ? <p>Loading...</p> : <p>Backend says: {message || 'No connection'}</p>}
        </div>
      </main>
      <Footer />
    </ThemeProvider>
  )
}

export default App
