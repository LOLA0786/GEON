import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Brain, Target, Zap, Users, TrendingUp, Shield } from "lucide-react";

export const About = () => {
  const features = [
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description:
        "Advanced machine learning algorithms analyze your website's structure, content, and performance patterns.",
    },
    {
      icon: Target,
      title: "Precision Optimization",
      description:
        "Get specific, actionable recommendations tailored to your website's unique characteristics and goals.",
    },
    {
      icon: Zap,
      title: "Instant Results",
      description:
        "Real-time analysis and suggestions delivered in seconds, not hours or days.",
    },
  ];

  const benefits = [
    {
      icon: Users,
      title: "For Developers",
      description:
        "Technical insights, code optimization suggestions, and performance improvements.",
    },
    {
      icon: TrendingUp,
      title: "For Marketers",
      description:
        "SEO recommendations, content optimization, and visibility enhancement strategies.",
    },
    {
      icon: Shield,
      title: "For Businesses",
      description:
        "Comprehensive website health reports and competitive advantage insights.",
    },
  ];
  const logos = [
    { src: "OpenAI.svg", alt: "OpenAI" },
    { src: "DeepSeek.svg", alt: "DeepSeek" },
    { src: "Gemini.svg", alt: "Gemini" },
    { src: "Meta.svg", alt: "Meta" },
    { src: "Perplexity.svg", alt: "Perplexity" },
    { src: "Claude.svg", alt: "Claude" },
  ];
  const [currentLogo, setCurrentLogo] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentLogo((prev) => (prev + 1) % logos.length);
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  return (
    <section className="py-20 relative">
      <div className="container mx-auto px-4">
        {/* What is GEO Section */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-20"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            What is GEON?
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Generative Engine Optimization is the next evolution of website
            optimization. Unlike traditional SEO, GEO uses AI to understand how
            generative engines and modern search algorithms interpret and rank
            your content.
          </p>
        </motion.div>

        {/* How It Works */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          viewport={{ once: true }}
          className="mb-24"
        >
          <h3 className="text-3xl font-bold text-center mb-12">How it Works</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ y: -5 }}
                className="text-center p-8 bg-card/30 backdrop-blur-sm rounded-lg border border-border/30 group"
              >
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary/10 rounded-full mb-6 group-hover:bg-primary/20 transition-colors">
                  <feature.icon className="w-8 h-8 text-primary" />
                </div>
                <h4 className="text-xl font-semibold mb-4">{feature.title}</h4>
                <p className="text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Benefits Section */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          viewport={{ once: true }}
          className="mb-24"
        >
          <h3 className="text-3xl font-bold text-center mb-12">
            Who Benefits from it?
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {benefits.map((benefit, index) => (
              <motion.div
                key={benefit.title}
                initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="p-8 bg-gradient-to-br from-card/50 to-card/20 backdrop-blur-sm rounded-lg border border-border/30 hover:border-primary/30 transition-colors"
              >
                <benefit.icon className="w-12 h-12 text-primary mb-6" />
                <h4 className="text-xl font-semibold mb-4">{benefit.title}</h4>
                <p className="text-muted-foreground leading-relaxed">
                  {benefit.description}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Neural Network Animation */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 1, delay: 0.6 }}
          viewport={{ once: true }}
          className="mt-24 mb-24 relative"
        >
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold mb-4">AI Neural Processing</h3>
            <p className="text-muted-foreground">
              Our AI continuously learns and improves optimization strategies
            </p>
          </div>

          <div className="relative h-40 overflow-hidden rounded-lg bg-gradient-to-r from-primary/5 to-accent/5 border border-border/30">
            {[...Array(8)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute w-2 h-2 bg-primary/60 rounded-full"
                animate={{
                  x: [-20, window.innerWidth || 1200],
                  y: [Math.random() * 120 + 20, Math.random() * 120 + 20],
                }}
                transition={{
                  duration: Math.random() * 4 + 3,
                  repeat: Infinity,
                  delay: Math.random() * 2,
                  ease: "linear",
                }}
                style={{
                  left: -20,
                  top: Math.random() * 120 + 20,
                }}
              />
            ))}

            {/* Neural connection lines */}
            <svg className="absolute inset-0 w-full h-full">
              {[...Array(5)].map((_, i) => (
                <motion.line
                  key={i}
                  x1={Math.random() * 100 + "%"}
                  y1={Math.random() * 100 + "%"}
                  x2={Math.random() * 100 + "%"}
                  y2={Math.random() * 100 + "%"}
                  stroke="hsl(var(--primary))"
                  strokeWidth="1"
                  strokeOpacity="0.3"
                  animate={{
                    strokeOpacity: [0.1, 0.5, 0.1],
                  }}
                  transition={{
                    duration: Math.random() * 2 + 1,
                    repeat: Infinity,
                    delay: Math.random(),
                  }}
                />
              ))}
            </svg>
          </div>
        </motion.div>

        {/* LLM Logos Section */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          viewport={{ once: true }}
          className="mt-24"
        >
          <h3 className="text-3xl sm:text-lg font-medium text-center mb-8">
            GEON is compatible with all major large language models including:
          </h3>
          <div className="flex justify-center items-center h-32">
            <AnimatePresence mode="wait">
              <motion.img
                key={logos[currentLogo].alt}
                src={logos[currentLogo].src}
                alt={logos[currentLogo].alt}
                className="h-16 object-contain"
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -20, scale: 0.95 }}
                transition={{ duration: 0.5 }}
              />
            </AnimatePresence>
          </div>
        </motion.div>
      </div>
    </section>
  );
};