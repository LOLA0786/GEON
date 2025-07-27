import { motion } from "framer-motion";
import { Brain, Zap, Shield, Target, Users, TrendingUp, Cpu, Network, Globe, ArrowLeftIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const AboutGEO = () => {
  const features = [
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description: "Advanced machine learning algorithms analyze your website's structure, content, and performance patterns to provide intelligent optimization recommendations."
    },
    {
      icon: Zap,
      title: "Instant Results",
      description: "Get comprehensive GEO analysis and optimization suggestions in seconds, not hours. Our real-time processing delivers actionable insights immediately."
    },
    {
      icon: Shield,
      title: "Enterprise Security",
      description: "Your data is protected with enterprise-grade security. We analyze your public-facing content without storing sensitive information."
    },
    {
      icon: Target,
      title: "Precision Optimization",
      description: "Receive specific, actionable recommendations tailored to your website's unique characteristics and business goals."
    },
    {
      icon: Users,
      title: "Multi-Stakeholder Value",
      description: "Whether you're a developer, marketer, or business owner, get insights that matter to your role and objectives."
    },
    {
      icon: TrendingUp,
      title: "Performance Tracking",
      description: "Monitor your GEO score improvements over time and track the impact of implemented optimizations."
    }
  ];

  const stats = [
    { number: "10,000+", label: "Websites Analyzed" },
    { number: "95%", label: "Score Improvement" },
    { number: "2.3s", label: "Average Analysis Time" },
    { number: "24/7", label: "AI Monitoring" }
  ];



  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border/40">
        <div className="container mx-auto px-4 py-4 flex">
          <Button variant="outline" asChild className="">
            <a href="/"><ArrowLeftIcon/></a>
          </Button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-5 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-accent/5" />
        <div className="container mx-auto px-4 relative">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center max-w-4xl mx-auto"
          >
            <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              About GEON
            </h1>
            <p className="text-xl text-muted-foreground mb-4 leading-relaxed">
              The future of website optimization powered by cutting-edge AI technology. 
              We're revolutionizing how businesses understand and improve their digital presence.
            </p>
            
            {/* Floating AI Elements */}
            <div className="relative h-20 mb-4">
              {[...Array(6)].map((_, i) => (
                <motion.div
                  key={i}
                  className="absolute w-2 h-2 bg-primary/60 rounded-full"
                  animate={{
                    x: [0, Math.random() * 200 - 100],
                    y: [0, Math.random() * 80 - 40],
                    opacity: [0.3, 1, 0.3],
                  }}
                  transition={{
                    duration: Math.random() * 3 + 2,
                    repeat: Infinity,
                    delay: Math.random() * 2,
                  }}
                  style={{
                    left: `${20 + i * 10}%`,
                    top: "50%",
                  }}
                />
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-6">Our Mission</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              To democratize advanced website optimization through AI, making enterprise-level 
              insights accessible to everyone from solo entrepreneurs to Fortune 500 companies.
            </p>
          </motion.div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-20">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <div className="text-4xl md:text-5xl font-bold text-primary mb-2">
                  {stat.number}
                </div>
                <div className="text-muted-foreground">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-6">Why Choose GEOscore?</h2>
            <p className="text-xl text-muted-foreground">
              Advanced AI technology meets intuitive design for unparalleled website optimization
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ y: -5 }}
              >
                <Card className="h-full bg-card/50 backdrop-blur-sm border-border/50 hover:border-primary/30 transition-all duration-300">
                  <CardContent className="p-8">
                    <div className="inline-flex items-center justify-center w-14 h-14 bg-primary/10 rounded-lg mb-6">
                      <feature.icon className="w-7 h-7 text-primary" />
                    </div>
                    <h3 className="text-xl font-semibold mb-4">{feature.title}</h3>
                    <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-6">Our Technology</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Built on the latest advances in machine learning, neural networks, and web analytics
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="text-center p-8 bg-gradient-to-br from-primary/10 to-accent/10 rounded-xl border border-border/30"
            >
              <Cpu className="w-16 h-16 text-primary mx-auto mb-6" />
              <h3 className="text-2xl font-bold mb-4">Neural Processing</h3>
              <p className="text-muted-foreground">
                Advanced neural networks trained on millions of web pages to understand modern optimization patterns
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              viewport={{ once: true }}
              className="text-center p-8 bg-gradient-to-br from-accent/10 to-primary/10 rounded-xl border border-border/30"
            >
              <Network className="w-16 h-16 text-accent mx-auto mb-6" />
              <h3 className="text-2xl font-bold mb-4">Real-Time Analysis</h3>
              <p className="text-muted-foreground">
                Lightning-fast processing pipeline that analyzes websites in seconds, not minutes
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              viewport={{ once: true }}
              className="text-center p-8 bg-gradient-to-br from-primary/10 to-accent/10 rounded-xl border border-border/30"
            >
              <Globe className="w-16 h-16 text-primary mx-auto mb-6" />
              <h3 className="text-2xl font-bold mb-4">Global Standards</h3>
              <p className="text-muted-foreground">
                Trained on international best practices and constantly updated with the latest optimization trends
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      {/* <section className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-6">Meet Our Team</h2>
            <p className="text-xl text-muted-foreground">
              World-class experts in AI, web development, and user experience
            </p>
          </motion.div> 

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {teamMembers.map((member, index) => (
              <motion.div
                key={member.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
                className="text-center p-8 bg-card/50 backdrop-blur-sm rounded-xl border border-border/30"
              >
                <div className="w-24 h-24 bg-gradient-to-br from-primary to-accent rounded-full mx-auto mb-6 flex items-center justify-center">
                  <span className="text-2xl font-bold text-white">{member.name.charAt(0)}</span>
                </div>
                <h3 className="text-xl font-bold mb-2">{member.name}</h3>
                <p className="text-primary font-medium mb-4">{member.role}</p>
                <p className="text-muted-foreground text-sm leading-relaxed">{member.description}</p>
              </motion.div>
            ))}
          </div> 
        </div>
      </section>*/}

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold mb-6">Ready to Optimize Your Website?</h2>
            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Join thousands of businesses already using GEON to improve their digital presence
            </p>
            <Button size="lg" className="bg-gradient-to-r from-primary to-accent hover:opacity-90" asChild>
              <a href="/">Start Your Free Analysis</a>
            </Button>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default AboutGEO;
