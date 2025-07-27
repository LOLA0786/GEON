import { motion } from "framer-motion";
import { Download, RefreshCw, BarChart3, TrendingUp, AlertTriangle, CheckCircle, Target, Zap, Eye, Link, Sparkles, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useState, useEffect, useRef } from "react";
import { GeoAnalysisService } from "@/services/geonService";
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

interface ResultsProps {
  websiteUrl?: string;
  data?: any;
  onReanalyze?: () => void;
}

export const Results = ({ websiteUrl = "example.com", data, onReanalyze }: ResultsProps) => {
  const [scores, setScores] = useState<any>(null);
  const [overallScore, setOverallScore] = useState<number>(0);
  const [loadingScores, setLoadingScores] = useState(true);
  const [downloadingPDF, setDownloadingPDF] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);
  
  // Extract data from API response
  const contentEval = data?.parsed_result?.content_geo_evaluation;
  const structureEval = data?.parsed_result?.structure_geo_evaluation;
  
  // Fetch scores on component mount
  useEffect(() => {
    const fetchScores = async () => {
      try {
        const scoresData = await GeoAnalysisService.getScores(websiteUrl);
        const parsedResult = (scoresData as { parsed_result?: { individual_scores?: any } }).parsed_result;
        const overallScoreObj = (scoresData as { parsed_result?: { final_geo_score?: number } }).parsed_result;
        const finalScore = overallScoreObj?.final_geo_score ?? 0;
        setOverallScore(finalScore);
        setScores(parsedResult?.individual_scores || {});
        console.log("scores", parsedResult?.individual_scores)
      } catch (error) {
        console.error('Failed to fetch scores:', error);
        // Set fallback scores
        setScores({
          content_quality: 85,
          structure_score: 78,
          entity_linking_score: 72,
          prompt_visibility: 90,
          response_alignment: 88,
          ai_readable_format: 80,
          freshness_score: 75
        });
      } finally {
        setLoadingScores(false);
      }
    };

    fetchScores();
  }, []);


  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-green-400";
    if (score >= 60) return "text-yellow-400";
    return "text-red-400";
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return "Excellent";
    if (score >= 60) return "Good";
    return "Needs Improvement";
  };

  // Calculate overall GEO score from individual scores

  // PDF generation function
  const generatePDF = async () => {
    if (!reportRef.current) return;
    setDownloadingPDF(true);
    try {
      const canvas = await html2canvas(reportRef.current, {
        scale: 2,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#fff'
      });
      
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF();
      const imgWidth = 210;
      const pageHeight = 295;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      let heightLeft = imgHeight;
      let position = 0;

      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;

      while (heightLeft >= 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }

      pdf.save(`GEO-Analysis-Report-${websiteUrl}.pdf`);
    } catch (error) {
      console.error('Error generating PDF:', error);
    } finally {
      setDownloadingPDF(false);
    }
  };

  // Score metrics with icons
  const scoreMetrics = [
    { key: "content_quality", label: "Content Quality", icon: Target },
    { key: "structure_score", label: "Structure Score", icon: BarChart3 },
    { key: "entity_linking_score", label: "Entity Linking", icon: Link },
    { key: "prompt_visibility", label: "Prompt Visibility", icon: Eye },
    { key: "response_alignment", label: "Response Alignment", icon: TrendingUp },
    { key: "ai_readable_format", label: "AI Readable Format", icon: Zap },
    { key: "freshness_score", label: "Freshness Score", icon: Clock }
  ];


  return (
    <section className="py-20">
      <div className="container mx-auto px-4" ref={reportRef} style={{
    background: downloadingPDF ? "#fff" : undefined,
    color: downloadingPDF ? "#222" : undefined,
    borderRadius: downloadingPDF ? "12px" : undefined,
    boxShadow: downloadingPDF ? "0 0 16px #eee" : undefined,
    padding: downloadingPDF ? "24px" : undefined,
  }}>
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            GEO Analysis Results
          </h1>
          <p className="text-xl text-muted-foreground">
            Analysis for <span className="text-primary font-semibold">{websiteUrl}</span>
          </p>
        </motion.div>

        {/* Top Section: Overall Score & Individual Scores */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 max-w-7xl mx-auto mb-12">
          {/* Overall GEO Score */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="lg:col-span-1"
          >
            <Card className="bg-card/50 backdrop-blur-sm border-border/50 text-center h-full">
              <CardHeader>
                <CardTitle className="text-lg">Overall GEO Score</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="relative w-24 h-24 mx-auto mb-4">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      stroke="hsl(var(--border))"
                      strokeWidth="8"
                      fill="none"
                    />
                    <motion.circle
                      cx="50"
                      cy="50"
                      r="40"
                      stroke="hsl(var(--primary))"
                      strokeWidth="8"
                      fill="none"
                      strokeLinecap="round"
                      initial={{ pathLength: 0 }}
                      animate={{ pathLength: overallScore / 100 }}
                      transition={{ duration: 2, ease: "easeOut" }}
                      style={{
                        strokeDasharray: "251",
                        strokeDashoffset: "251",
                      }}
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <motion.span
                      className={`text-2xl font-bold ${getScoreColor(overallScore)}`}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 2 }}
                    >
                      {overallScore}
                    </motion.span>
                  </div>
                </div>
                <Badge variant="outline" className={`${getScoreColor(overallScore)} border-current`}>
                  {getScoreLabel(overallScore)}
                </Badge>
              </CardContent>
            </Card>
          </motion.div>

          {/* Individual Scores */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="lg:col-span-3"
          >
            <Card className="bg-card/50 backdrop-blur-sm border-border/50 h-full">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-primary" />
                  Detailed Score Breakdown
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {scoreMetrics.map((metric, index) => (
                    <motion.div
                      key={metric.key}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
                      className="flex items-center gap-3 p-3 bg-background/30 rounded-lg"
                    >
                      <metric.icon className="w-5 h-5 text-primary" />
                      <div>
                        <div className={`text-lg font-semibold ${getScoreColor(scores?.[metric.key] || 0)}`}>
                          {loadingScores ? "..." : scores?.[metric.key] || 0}
                        </div>
                        <div className="text-xs text-muted-foreground">{metric.label}</div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Content & Structure Analysis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          {/* Content Analysis */}
          {contentEval && (
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
            >
              <Card className="bg-card/50 backdrop-blur-sm border-border/50 h-full">
                <CardHeader>
                  <CardTitle className="text-xl flex items-center gap-2">
                    <Target className="w-6 h-6 text-green-400" />
                    Content Evaluation
                    {/* <Badge variant="outline" className={`${getScoreColor(contentEval.geo_score)} border-current ml-auto`}>
                      {contentEval.geo_score}/100
                    </Badge> */}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Strengths */}
                  {contentEval.strengths && contentEval.strengths.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-green-400 flex items-center gap-2 mb-3">
                        <CheckCircle className="w-4 h-4" />
                        Strengths ({contentEval.strengths.length})
                      </h4>
                      <div className="space-y-2">
                        {contentEval.strengths.map((strength: string, index: number) => (
                          <div key={index} className="text-sm text-muted-foreground p-2 bg-green-500/5 rounded border-l-2 border-green-400">
                            {strength}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Improvements */}
                  {contentEval.improvements && contentEval.improvements.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-yellow-400 flex items-center gap-2 mb-3">
                        <AlertTriangle className="w-4 h-4" />
                        Areas for Improvement ({contentEval.improvements.length})
                      </h4>
                      <div className="space-y-2">
                        {contentEval.improvements.map((improvement: string, index: number) => (
                          <div key={index} className="text-sm text-muted-foreground p-2 bg-yellow-500/5 rounded border-l-2 border-yellow-400">
                            {improvement}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Notes */}
                  {contentEval.notes && (
                    <div className="p-3 bg-blue-500/5 rounded border-l-2 border-blue-400">
                      <h4 className="font-semibold text-blue-400 mb-2">Analysis Notes</h4>
                      <p className="text-sm text-muted-foreground">{contentEval.notes}</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          )}

          {/* Structure Analysis */}
          {structureEval && (
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.8 }}
            >
              <Card className="bg-card/50 backdrop-blur-sm border-border/50 h-full">
                <CardHeader>
                  <CardTitle className="text-xl flex items-center gap-2">
                    <BarChart3 className="w-6 h-6 text-blue-400" />
                    Structure Evaluation
                    {/* <Badge variant="outline" className={`${getScoreColor(structureEval.geo_score)} border-current ml-auto`}>
                      {structureEval.geo_score}/100
                    </Badge> */}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Strengths */}
                  {structureEval.strengths && structureEval.strengths.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-green-400 flex items-center gap-2 mb-3">
                        <CheckCircle className="w-4 h-4" />
                        Strengths ({structureEval.strengths.length})
                      </h4>
                      <div className="space-y-2">
                        {structureEval.strengths.map((strength: string, index: number) => (
                          <div key={index} className="text-sm text-muted-foreground p-2 bg-green-500/5 rounded border-l-2 border-green-400">
                            {strength}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Improvements */}
                  {structureEval.improvements && structureEval.improvements.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-yellow-400 flex items-center gap-2 mb-3">
                        <AlertTriangle className="w-4 h-4" />
                        Areas for Improvement ({structureEval.improvements.length})
                      </h4>
                      <div className="space-y-2">
                        {structureEval.improvements.map((improvement: string, index: number) => (
                          <div key={index} className="text-sm text-muted-foreground p-2 bg-yellow-500/5 rounded border-l-2 border-yellow-400">
                            {improvement}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Notes */}
                  {structureEval.notes && (
                    <div className="p-3 bg-blue-500/5 rounded border-l-2 border-blue-400">
                      <h4 className="font-semibold text-blue-400 mb-2">Analysis Notes</h4>
                      <p className="text-sm text-muted-foreground">{structureEval.notes}</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 1.0 }}
          className="flex flex-col sm:flex-row gap-4 justify-center mt-12"
        >
          <Button 
            className="primary-button" 
            size="lg"
            onClick={generatePDF}
            disabled={downloadingPDF}
          >
            <Download className="w-5 h-5 mr-2" />
            {downloadingPDF ? "Generating PDF..." : "Download PDF Report"}
          </Button>
          <Button variant="outline" size="lg" className="border-border/50 hover:border-primary/50" onClick={onReanalyze}>
            <RefreshCw className="w-5 h-5 mr-2" />
            Re-analyze Website
          </Button>
        </motion.div>
      </div>
    </section>
  );
};