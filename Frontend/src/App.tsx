import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import { Results } from "./components/Results";
import AboutGEO from "./components/AboutGEO";
import SignUp from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import SignIn from "./pages/SignIn";
import { Toaster } from "react-hot-toast";
import AfterSignUp from "./pages/AfterSignUp";
import { AnalysisLoading } from "./components/AnalysisLoading";
// import {authContext} from "./hooks/useAuth.js"


const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      {/* <authContext.Provider> */}
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<><Navbar/><Index /><Footer/></>} />
          <Route path="/signup" element={<><SignUp/></>}/>
          <Route path="/signin" element={<><SignIn/></>}/>
          <Route path="/results" element={<><Navbar/><Results/><Footer/></>}/>
          <Route path="/dashboard" element={<><Dashboard/><Footer/></>}/>
          <Route path="/about" element={<><Navbar/><AboutGEO/><Footer/></>}/>
          <Route path="*" element={<><Navbar/><NotFound /></>} />
          <Route path="/analyzing" element={<AnalysisLoading url={""} onComplete={function (): void {
            throw new Error("Function not implemented.");
          } }/>}/>
        </Routes>
      </BrowserRouter>
      {/* </authContext.Provider> */}
     <Toaster/>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
