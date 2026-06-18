import { Link } from 'react-router-dom'

export default function Navbar() {
  const adminToken = localStorage.getItem('admin_token')

  return (
    <nav className="flex justify-between items-center px-6 py-4 bg-white shadow-sm">
      <Link to="/" className="font-bold text-lg text-indigo-600">
        SocialBunny
      </Link>
      <div className="flex gap-4 text-sm">
        <Link to="/register" className="text-gray-600 hover:text-indigo-600">
          Register
        </Link>
        {adminToken ? (
          <Link to="/admin/dashboard" className="text-indigo-600 font-medium">
            Dashboard
          </Link>
        ) : (
          <Link to="/admin/login" className="text-gray-600 hover:text-indigo-600">
            Admin Login
          </Link>
        )}
      </div>
    </nav>
  )
}
