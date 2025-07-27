import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Menu, X , ArrowRight, ChevronRight} from "lucide-react";
import { Button } from "./ui/button";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const [isOpen, setIsOpen] = React.useState(false);
  const [scrolled, setScrolled] = React.useState(false);
  const navigate = useNavigate();

  return (
    <motion.header
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
      className={`sticky top-0 z-50 shadow-md transition-all duration-300 bg-black backdrop-blur-sm
  `}
    >
      <div className="bg-max-w-7xl mx-auto mb-10 lg:mb-0 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/"><img src="/logo.png" alt="GEON Logo" className="w-auto h-32 md:h-44 lg:h-52" /></Link>
            <span className="text-xl font-bold text-gray-800"></span>
          </div>

          {/* Desktop Nav */}
          <nav className="items-center hidden md:flex space-x-14 pr-20">
            <Link
              to="/"
              className="text-white hover:text-blue-500 font-medium transition"
            >
              Home
            </Link>
            <Link
              to="/resources"
              className="text-white hover:text-blue-500 font-medium transition"
            >
              Resources
            </Link>
            <Link
              to="/about"
              className="text-white hover:text-blue-500 font-medium transition"
            >
              About
            </Link>
            <Link
              to="/features"
              className="text-white hover:text-blue-500 font-medium transition"
            >
              Features
            </Link>
            <Link
              to="/careers"
              className="text-white hover:text-blue-500 font-medium transition"
            >
              Careers
            </Link>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate("/signup")}
              className="border border-blue-500 hover:bg-blue-100 text-blue-500 px-3 py-2 rounded-sm text-base flex justify-center items-center"
            >
              Get Started <ChevronRight className="size-5"/>
            </motion.button>
          </nav>

          {/* Mobile Menu Button */}
          <div className="md:hidden mr-4">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-600 hover:text-blue-600"
            >
              {isOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
  <motion.div
    initial={{ opacity: 0, y: -20 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -20 }}
    transition={{ duration: 0.3 }}
    className="fixed inset-0 z-50 bg-[hsl(220_20%_8%)] bg-opacity-95 backdrop-blur-md p-6 flex flex-col items-center justify-center space-y-6 md:hidden"
  >
    <Link to="/" className="text-white text-xl hover:text-blue-400" onClick={() => setIsOpen(false)}>
      Home
    </Link>
    <Link to="/resources" className="text-white text-xl hover:text-blue-400" onClick={() => setIsOpen(false)}>
      Resources
    </Link>
    <Link to="/about" className="text-white text-xl hover:text-blue-400" onClick={() => setIsOpen(false)}>
      About
    </Link>
    <Link to="/features" className="text-white text-xl hover:text-blue-400" onClick={() => setIsOpen(false)}>
      Features
    </Link>
    <Link to="/contact" className="text-white text-xl hover:text-blue-400" onClick={() => setIsOpen(false)}>
      Contact
    </Link>
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className="mt-4 bg-blue-500 text-white px-6 py-2 rounded"
      onClick={() => setIsOpen(false)}
    >
      Get Started <ChevronLeft/>
    </motion.button>
  </motion.div>
)}
    </motion.header>
  );
};

export default Navbar;
