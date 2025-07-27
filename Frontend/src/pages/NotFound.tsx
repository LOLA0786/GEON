import { useLocation } from "react-router-dom";
import { useEffect } from "react";
import { motion } from "framer-motion";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="h-screen bg-[hsl(220_20%_8%)] flex items-center justify-center px-4">
      <motion.div
        className="text-center mb-48"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="text-7xl md:text-9xl font-extrabold text-white mb-4">404</h1>
        <p className="text-xl md:text-2xl text-gray-400 mb-6">
          Oops! The page you're looking for doesn't exist.
        </p>
        <a
          href="/"
          className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-full transition duration-300"
        >
          Go to Homepage
        </a>
      </motion.div>
    </div>
  );
};

export default NotFound;
