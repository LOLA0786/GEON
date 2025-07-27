// import { Hero } from "./Hero";
// import { About } from "./About";
// import { Contact } from "./Contact";
// import { Results } from "./Results";
// import { useState } from "react";
// import FaqSection from "./FaqSection"

// export const Dashboard = () => {
//   const [showResults, setShowResults] = useState(false);
//   const [analyzedUrl, setAnalyzedUrl] = useState("");

//   // This would be triggered from the Hero component's analyze function
//   const handleShowResults = (url: string) => {
//     setAnalyzedUrl(url);
//     setShowResults(true);
//   };

//   if (showResults) {
//     return <Results websiteUrl={analyzedUrl} />;
//   }

//   return (
//     <div className="min-h-screen bg-background">
//       <Hero />
//       <About />
//       <FaqSection/>
//       <Contact />
//     </div>
//   );
// };
import { Hero } from "./Hero";
import {About}  from "./About";
import { Contact } from "./Contact";
import { Results } from "./Results";
import { AnalysisLoading } from "./AnalysisLoading";
import { useState } from "react";
import FaqSection from "./FaqSection";
import { useNavigate } from "react-router-dom";

type DashboardState = 'home' | 'analyzing' | 'results';


export const Dashboard = () => {
  const [currentState, setCurrentState] = useState<DashboardState>('home');
  const [analysisResults, setAnalysisResults] = useState<any>(null);
  const [analyzedUrl, setAnalyzedUrl] = useState("");
  const navigate = useNavigate();

  const handleAnalyze = (url: string) => {
    setAnalyzedUrl(url);
    setCurrentState('analyzing');
  };
  const handleReanalyze = () => {
    setCurrentState('analyzing');
  }

  const handleAnalysisComplete = (results: unknown) => {
    setCurrentState('results');
    setAnalysisResults(results);
  };

  if (currentState === 'analyzing') {
    // navigate("/analyzing");
    return <AnalysisLoading url={analyzedUrl} onComplete={handleAnalysisComplete} />;
  }

  if (currentState === 'results') {
    // navigate("/results");
    return <Results websiteUrl={analyzedUrl} data={analysisResults} onReanalyze={handleReanalyze}/>;
  }

  return (
    <div className="min-h-screen bg-background">
      <Hero onAnalyze={handleAnalyze} />
      <About />
      <FaqSection/>
      <Contact />
    </div>
  );
};