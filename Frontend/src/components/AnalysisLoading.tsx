import { motion } from "framer-motion";
import { Globe, Search, Brain, Zap, CheckCircle } from "lucide-react";
import { useEffect, useState } from "react";
import { GeoAnalysisService } from "@/services/geonService";
// import { useToast } from "@/hooks/use-toast";
import {toast} from "react-hot-toast";
import { redirect, useNavigate } from "react-router-dom";

interface AnalysisLoadingProps {
    url: string,
    onComplete: (results: unknown) => void;
}

type AnalysisStage = "scraping" | "parsing" | "analysing" | "complete" | "error";

export const AnalysisLoading = ({url, onComplete }: AnalysisLoadingProps) => {
  const [currentStage, setCurrentStage] = useState<AnalysisStage>("scraping");
  const [error, setError] = useState({});
  const navigate = useNavigate();

useEffect(() => {
    const analyzeWebsite = async () => {
      try {
        setCurrentStage('scraping');

        // Call scrape API
        const scrapeResult = await GeoAnalysisService
        .scrapeWebsite(url);
        setCurrentStage('parsing');
        if(scrapeResult.cleaned_dom==''){
            toast.error("Please enter a correct URL!")
            
            return;
        }

        // Call parse API with session ID
        const parseResult = await GeoAnalysisService
        .parseWebsite(scrapeResult.session_id);
        setCurrentStage('complete');

        // Wait a moment to show completion, then call onComplete with results
        setTimeout(() => {
          onComplete(parseResult);
        }, 1500);

      } catch (error) {
        console.error('Analysis failed:', error);

        setError(error instanceof Error ? error.message : 'Analysis failed');
        setCurrentStage('error');
        toast.error("Analysis failed!")
      }
    };

    analyzeWebsite();
  }, [url, onComplete, toast]);


  const stages = [
    {
      id: "scraping",
      icon: Search,
      title: "Scraping Website",
      description: "Analyzing site structure and content...",
      color: "text-blue-500",
    },
    {
      id: "parsing",
      icon: Brain,
      title: "AI Processing",
      description: "Generating optimization insights...",
      color: "text-purple-500",
    },
    {
      id: "analysing",
      icon: Zap,
      title: "Analysing Score",
      description: " Calculating GEO score and metrics...",
      color: "text-yellow-500",
    },
    {
      id: "complete",
      icon: CheckCircle,
      title: "Analysis Complete",
      description: "Preparing your results...",
      color: "text-green-500",
    },
  ];

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="max-w-2xl mx-auto p-8 text-center">

        {/* Stages */}
        <div className="space-y-6">
          {stages.map((stage, index) => {
            const isActive = stage.id === currentStage;
            const isCompleted =
              (stage.id === "scraping" &&
                (currentStage === "parsing" || currentStage === "analysing" || currentStage === "complete")) ||
              (stage.id === "parsing" &&
                (currentStage === "analysing" || currentStage === "complete")) ||
              (stage.id === "analysing" && currentStage === "complete");

            return (
              <motion.div
                key={stage.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.2 }}
                className={`flex items-center gap-6 px-8 py-4 rounded-lg border transition-all duration-500 ${
                  isActive
                    ? "bg-primary/10 border-primary/30 shadow-lg"
                    : isCompleted
                    ? "bg-green-500/10 border-green-500/30"
                    : "bg-card/30 border-border/30"
                }`}
              >
                <div
                  className={`flex-shrink-0 ${
                    isActive
                      ? stage.color
                      : isCompleted
                      ? "text-green-500"
                      : "text-muted-foreground"
                  }`}
                >
                  {isActive ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "linear",
                      }}
                    >
                      <stage.icon className="w-8 h-8" />
                    </motion.div>
                  ) : (
                    <stage.icon className="w-8 h-8" />
                  )}
                </div>

                <div className="text-left">
                  <h3
                    className={`text-lg font-semibold mb-1 ${
                      isActive
                        ? "text-foreground"
                        : isCompleted
                        ? "text-green-600"
                        : "text-muted-foreground"
                    }`}
                  >
                    {stage.title}
                  </h3>
                  <p className="text-sm text-muted-foreground">
                    {stage.description}
                  </p>
                </div>

                {isActive && (
                  <motion.div
                    className="ml-auto flex gap-1"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                  >
                    {[...Array(3)].map((_, i) => (
                      <motion.div
                        key={i}
                        className="w-2 h-2 bg-primary rounded-full"
                        animate={{ scale: [1, 1.5, 1] }}
                        transition={{
                          duration: 0.6,
                          repeat: Infinity,
                          delay: i * 0.2,
                        }}
                      />
                    ))}
                  </motion.div>
                )}

                {isCompleted && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="ml-auto"
                  >
                    <CheckCircle className="w-6 h-6 text-green-500" />
                  </motion.div>
                )}
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
