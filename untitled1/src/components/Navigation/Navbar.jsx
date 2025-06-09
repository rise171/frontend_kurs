import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.jsx';
import './Navbar.css';
import { MdOutlineDateRange } from "react-icons/md";
import { BiSupport } from "react-icons/bi";
import { FaAddressBook, FaSignOutAlt, FaBars } from "react-icons/fa";
import { FaQuestion } from "react-icons/fa";
import { FaHome } from "react-icons/fa";
import { GrUserAdmin } from "react-icons/gr";

const Navbar = () => {
  const { logout, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const closeSidebar = () => {
    setIsSidebarOpen(false);
  };

  return (
    <>
      <nav className="navbar">
        <button className="menu-toggle" onClick={toggleSidebar}>
          <FaBars />
        </button>
        <div className="navbar-brand">
          <h1>Психологический сервис</h1>
        </div>
        <div className={`navbar-links ${isSidebarOpen ? 'sidebar-open' : ''}`}>
          <div className="sidebar-header">
            <h2>Меню</h2>
            <button className="close-sidebar" onClick={closeSidebar}>×</button>
          </div>
          {isAdmin() ? (
            <Link to="/admin" className="nav-link admin-link" onClick={closeSidebar}>
              <GrUserAdmin className="nav-icon" />
              <span>Административная панель</span>
            </Link>
          ) : (
            <Link to="/user" className="nav-link" onClick={closeSidebar}>
              <FaHome className="nav-icon" />
              <span>Личный кабинет</span>
            </Link>
          )}
          <Link to="/tests" className="nav-link" onClick={closeSidebar}>
            <FaQuestion className="nav-icon" />
            <span>Тесты</span>
          </Link>
          <Link to="/calendar" className="nav-link" onClick={closeSidebar}>
            <MdOutlineDateRange className="nav-icon" />
            <span>Календарь</span>
          </Link>
          <Link to="/thoughts" className="nav-link" onClick={closeSidebar}>
            <FaAddressBook className="nav-icon" />
            <span>Дневник мыслей</span>
          </Link>
          <Link to="/feedback" className="nav-link" onClick={closeSidebar}>
            <BiSupport className="nav-icon" />
            <span>Обратная связь</span>
          </Link>
          <button onClick={() => { handleLogout(); closeSidebar(); }} className="logout-button">
            <FaSignOutAlt className="nav-icon" />
            <span>Выйти</span>
          </button>
        </div>
      </nav>
      {isSidebarOpen && <div className="sidebar-overlay" onClick={closeSidebar}></div>}
    </>
  );
};

export default Navbar; 