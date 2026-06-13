/** @jsxImportSource @emotion/react */
import styled from '@emotion/styled'

const Bar = styled.nav`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: white;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
`

export default function Navbar() {
  return (
    <Bar>
      <span style={{ fontWeight: 700, color: '#2563eb' }}>ReactBoiler</span>
      <div style={{ display: 'flex', gap: 16 }}>
        <a href="#features">Features</a>
        <a href="#docs">Docs</a>
        <a href="#about">About</a>
      </div>
    </Bar>
  )
}
