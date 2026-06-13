import { motion } from 'framer-motion'

export default function Hero({ title, subtitle }) {
  return (
    <section style={{ padding: '4rem 0' }}>
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        style={{ fontSize: '3rem', marginBottom: '1rem', background: 'linear-gradient(135deg,#667eea,#764ba2)', WebkitBackgroundClip: 'text', color: 'transparent' }}
      >
        {title}
      </motion.h1>
      <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} style={{ color: '#555', fontSize: '1.1rem' }}>
        {subtitle}
      </motion.p>
    </section>
  )
}
