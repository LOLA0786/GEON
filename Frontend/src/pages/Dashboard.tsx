import { useState } from "react";
import { motion } from "framer-motion";
import { 
  BarChart3, 
  TrendingUp, 
  Search, 
  Zap, 
  Globe, 
  Users, 
  Target,
  Settings,
  LogOut,
  Menu,
  X,
  ChevronDown,
  MoreHorizontal,
  Filter,
  Calendar,
  Download,
  Bell,
  User,
  ChevronRight,
  Eye,
  Clock,
  ArrowUpRight
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { MetricCard } from "@/components/MetricCard";
import { ChartSection } from "@/components/ChartSection";

const sidebarItems = [
  { name: "Overview", icon: BarChart3, active: true, href: "/dashboard" },
  { name: "Website Analysis", icon: Search, active: false, href: "/analyzer" },
  { name: "GEO Optimization", icon: Zap, active: false, href: "/optimization", hasSubmenu: true },
  { name: "Performance Monitoring", icon: TrendingUp, active: false, href: "/performance" },
  { name: "Competitor Analysis", icon: Globe, active: false, href: "/competitors" },
  { name: "Audience Insights", icon: Users, active: false, href: "/audience" },
  { name: "Content Strategy", icon: Target, active: false, href: "/content" },
  { name: "Settings", icon: Settings, active: false, href: "/settings" },
];

// Realistic performance data with more detail
const performanceData = [
  { name: "Oct 15", value: 67.2 },
  { name: "Oct 22", value: 71.8 },
  { name: "Oct 29", value: 69.4 },
  { name: "Nov 5", value: 74.1 },
  { name: "Nov 12", value: 78.6 },
  { name: "Nov 19", value: 82.3 },
  { name: "Nov 26", value: 79.7 },
  { name: "Dec 3", value: 84.2 },
  { name: "Dec 10", value: 86.8 },
  { name: "Dec 17", value: 88.4 },
];

const visibilityData = [
  { name: "Week 42", value: 43.2 },
  { name: "Week 43", value: 48.7 },
  { name: "Week 44", value: 52.1 },
  { name: "Week 45", value: 58.9 },
  { name: "Week 46", value: 64.7 },
  { name: "Week 47", value: 61.3 },
  { name: "Week 48", value: 67.8 },
];

// Real-looking website data
const topWebsites = [
  { 
    rank: 1, 
    domain: "techcrunch.com", 
    score: 94.2, 
    trend: "+2.3%", 
    category: "Technology",
    lastAnalyzed: "2 hours ago",
    traffic: "2.4M"
  },
  { 
    rank: 2, 
    domain: "medium.com", 
    score: 91.8, 
    trend: "+1.7%", 
    category: "Publishing",
    lastAnalyzed: "4 hours ago",
    traffic: "1.8M"
  },
  { 
    rank: 3, 
    domain: "shopify.com", 
    score: 89.5, 
    trend: "-0.8%", 
    category: "E-commerce",
    lastAnalyzed: "6 hours ago",
    traffic: "3.2M"
  },
  { 
    rank: 4, 
    domain: "hubspot.com", 
    score: 87.1, 
    trend: "+3.2%", 
    category: "Marketing",
    lastAnalyzed: "1 hour ago",
    traffic: "1.1M"
  },
  { 
    rank: 5, 
    domain: "stripe.com", 
    score: 85.9, 
    trend: "+1.4%", 
    category: "Fintech",
    lastAnalyzed: "3 hours ago",
    traffic: "892K"
  },
];

export default function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [expandedItems, setExpandedItems] = useState<string[]>([]);

  const toggleSubmenu = (itemName: string) => {
    setExpandedItems(prev => 
      prev.includes(itemName) 
        ? prev.filter(item => item !== itemName)
        : [...prev, itemName]
    );
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <motion.aside 
        className={`fixed left-0 top-0 h-full bg-card border-r border-border z-50 transition-all duration-300 ${
          sidebarOpen ? "w-72" : "w-16"
        }`}
        initial={{ x: -100 }}
        animate={{ x: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="p-6 border-b border-border">
          <div className="flex items-center justify-between">
            {sidebarOpen && (
              <motion.div 
                className="flex items-center gap-3"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                <div className="w-10 h-10 bg-gradient-primary rounded-xl flex items-center justify-center shadow-lg">
                  <Zap className="w-5 h-5 text-white" />
                </div>
                <div>
                  <span className="text-xl font-bold text-gradient-primary">GEOscore</span>
                  <div className="text-xs text-muted-foreground">Analytics Platform</div>
                </div>
              </motion.div>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-muted/50"
            >
              {sidebarOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
            </Button>
          </div>
        </div>

        <div className="p-4">
          {sidebarOpen && (
            <div className="mb-6 p-3 bg-gradient-to-r from-primary/5 to-primary/10 rounded-xl border border-primary/20">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">Live Analytics</span>
              </div>
              <div className="text-xs text-muted-foreground">
                287 websites being monitored
              </div>
            </div>
          )}
        </div>

        <nav className="px-4 space-y-2">
          {sidebarItems.map((item) => (
            <div key={item.name}>
              <motion.div
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer transition-all duration-200 ${
                  item.active 
                    ? "bg-primary text-primary-foreground shadow-md" 
                    : "hover:bg-muted/60 text-muted-foreground hover:text-foreground"
                }`}
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                onClick={() => item.hasSubmenu && toggleSubmenu(item.name)}
              >
                <item.icon className="w-5 h-5 flex-shrink-0" />
                {sidebarOpen && (
                  <>
                    <span className="text-sm font-medium flex-1">{item.name}</span>
                    {item.hasSubmenu && (
                      <ChevronDown 
                        className={`w-4 h-4 transition-transform ${
                          expandedItems.includes(item.name) ? "rotate-180" : ""
                        }`} 
                      />
                    )}
                  </>
                )}
              </motion.div>
              
              {sidebarOpen && item.hasSubmenu && expandedItems.includes(item.name) && (
                <motion.div 
                  className="ml-8 mt-2 space-y-1"
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                >
                  <div className="text-xs text-muted-foreground p-2 hover:text-foreground cursor-pointer rounded-lg hover:bg-muted/30">Content Optimization</div>
                  <div className="text-xs text-muted-foreground p-2 hover:text-foreground cursor-pointer rounded-lg hover:bg-muted/30">Technical Analysis</div>
                  <div className="text-xs text-muted-foreground p-2 hover:text-foreground cursor-pointer rounded-lg hover:bg-muted/30">Keyword Research</div>
                </motion.div>
              )}
            </div>
          ))}
        </nav>
        
        {sidebarOpen && (
          <div className="absolute bottom-6 left-4 right-4 space-y-4">
            <div className="p-3 bg-muted/30 rounded-xl">
              <div className="flex items-center gap-3 mb-2">
                <Avatar className="w-8 h-8">
                  <AvatarImage src="" />
                  <AvatarFallback className="bg-primary text-primary-foreground text-xs">JD</AvatarFallback>
                </Avatar>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium truncate">John Doe</div>
                  <div className="text-xs text-muted-foreground">Premium Plan</div>
                </div>
              </div>
            </div>
            
            <motion.div
              className="flex items-center gap-3 p-3 rounded-xl cursor-pointer hover:bg-destructive/10 text-muted-foreground hover:text-destructive transition-colors"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <LogOut className="w-5 h-5 flex-shrink-0" />
              <span className="text-sm font-medium">Sign Out</span>
            </motion.div>
          </div>
        )}
      </motion.aside>

      {/* Main Content */}
      <div className={`transition-all duration-300 ${sidebarOpen ? "ml-72" : "ml-16"}`}>
        {/* Header */}
        <header className="bg-card/80 backdrop-blur-sm border-b border-border p-6 sticky top-0 z-40">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3 mb-1">
                <h1 className="text-2xl font-bold text-foreground">Dashboard Overview</h1>
                <Badge variant="secondary" className="text-xs">
                  <div className="w-1.5 h-1.5 bg-green-500 rounded-full mr-1.5"></div>
                  Live
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground flex items-center gap-2">
                <Clock className="w-4 h-4" />
                Last updated: December 19, 2025 at 2:04 PM EST
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Button variant="outline" size="sm" className="gap-2">
                <Calendar className="w-4 h-4" />
                Last 30 days
                <ChevronDown className="w-3 h-3" />
              </Button>
              <Button variant="outline" size="sm" className="gap-2">
                <Filter className="w-4 h-4" />
                Filter
              </Button>
              <Button variant="outline" size="sm" className="gap-2">
                <Download className="w-4 h-4" />
                Export
              </Button>
              <Button variant="outline" size="icon" className="relative">
                <Bell className="w-4 h-4" />
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full text-[10px] text-white flex items-center justify-center">3</div>
              </Button>
            </div>
          </div>
        </header>

        {/* Content */}
        <main className="p-6 space-y-8">
          {/* Metrics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <MetricCard
              title="Overall GEO Score"
              value="86.2"
              trend={3.2}
              trendDirection="up"
              icon={<Target className="w-5 h-5 text-primary" />}
            />
            <MetricCard
              title="Search Visibility"
              value="64.7%"
              trend={2.4}
              trendDirection="down"
              icon={<Eye className="w-5 h-5 text-blue-500" />}
            />
            <MetricCard
              title="Performance Score"
              value="92.4"
              trend={8.1}
              trendDirection="up"
              icon={<TrendingUp className="w-5 h-5 text-green-500" />}
            />
            <MetricCard
              title="Websites Monitored"
              value="287"
              trend={12.3}
              trendDirection="up"
              icon={<Globe className="w-5 h-5 text-purple-500" />}
            />
          </div>

          {/* Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChartSection
              title="GEO Performance Trends"
              subtitle="Weekly performance analysis over the last 10 weeks"
              data={performanceData}
              color="hsl(var(--primary))"
            />
            <ChartSection
              title="Search Visibility Trends"
              subtitle="7-day rolling average visibility metrics"
              data={visibilityData}
              color="hsl(217, 91%, 60%)"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Top Performing Websites */}
            <Card className="lg:col-span-2">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center gap-2">
                    <Target className="w-5 h-5" />
                    Top Performing Websites
                  </CardTitle>
                  <Button variant="ghost" size="sm" className="gap-1 text-muted-foreground">
                    View all <ChevronRight className="w-3 h-3" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {topWebsites.map((website) => (
                    <div key={website.rank} className="group flex items-center justify-between p-4 rounded-xl bg-muted/20 hover:bg-muted/40 transition-all duration-200 border border-transparent hover:border-border">
                      <div className="flex items-center gap-4">
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                            website.rank === 1 ? 'bg-yellow-100 text-yellow-700 border-2 border-yellow-300' :
                            website.rank === 2 ? 'bg-gray-100 text-gray-700 border-2 border-gray-300' :
                            website.rank === 3 ? 'bg-orange-100 text-orange-700 border-2 border-orange-300' :
                            'bg-muted text-muted-foreground'
                          }`}>
                            {website.rank}
                          </div>
                          <div>
                            <div className="font-semibold text-foreground group-hover:text-primary transition-colors">
                              {website.domain}
                            </div>
                            <div className="flex items-center gap-3 text-xs text-muted-foreground">
                              <span>{website.category}</span>
                              <span>•</span>
                              <span>{website.traffic} monthly visits</span>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <div className="font-bold text-lg">{website.score}</div>
                          <div className="text-xs text-muted-foreground">{website.lastAnalyzed}</div>
                        </div>
                        <div className={`px-2.5 py-1.5 rounded-lg text-sm font-medium ${
                          website.trend.startsWith('+') 
                            ? 'text-green-700 bg-green-100 border border-green-200' 
                            : 'text-red-700 bg-red-100 border border-red-200'
                        }`}>
                          {website.trend}
                        </div>
                        <Button variant="ghost" size="icon" className="w-8 h-8 opacity-0 group-hover:opacity-100 transition-opacity">
                          <ArrowUpRight className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* GEO Impact Assessment */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  GEO Impact Distribution
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-4">
                  <div className="relative">
                    <div className="p-4 rounded-xl bg-gradient-to-br from-red-50 to-red-100 border border-red-200">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-red-700 font-semibold text-sm">Critical Issues</div>
                        <div className="text-red-600 text-xs bg-red-200 px-2 py-1 rounded-full">+5 this week</div>
                      </div>
                      <div className="text-3xl font-bold text-red-700 mb-1">23</div>
                      <div className="text-red-600 text-xs">Websites requiring immediate attention</div>
                    </div>
                  </div>
                  
                  <div className="relative">
                    <div className="p-4 rounded-xl bg-gradient-to-br from-yellow-50 to-yellow-100 border border-yellow-200">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-yellow-700 font-semibold text-sm">Needs Improvement</div>
                        <div className="text-yellow-600 text-xs bg-yellow-200 px-2 py-1 rounded-full">+11 this week</div>
                      </div>
                      <div className="text-3xl font-bold text-yellow-700 mb-1">87</div>
                      <div className="text-yellow-600 text-xs">Moderate optimization opportunities</div>
                    </div>
                  </div>
                  
                  <div className="relative">
                    <div className="p-4 rounded-xl bg-gradient-to-br from-green-50 to-green-100 border border-green-200">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-green-700 font-semibold text-sm">Performing Well</div>
                        <div className="text-green-600 text-xs bg-green-200 px-2 py-1 rounded-full">+40 this week</div>
                      </div>
                      <div className="text-3xl font-bold text-green-700 mb-1">177</div>
                      <div className="text-green-600 text-xs">Websites meeting GEO standards</div>
                    </div>
                  </div>
                </div>
                
                <div className="pt-4 border-t border-border">
                  <div className="text-sm text-muted-foreground mb-2">Total Analyzed</div>
                  <div className="text-2xl font-bold">287</div>
                  <div className="text-xs text-muted-foreground">websites in your portfolio</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Recent Activity & Quick Actions */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="w-5 h-5" />
                  Recent Analysis Activity
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { action: "GEO analysis completed", website: "techcrunch.com", time: "2 minutes ago", status: "success" },
                    { action: "Performance scan started", website: "medium.com", time: "15 minutes ago", status: "processing" },
                    { action: "Optimization suggestions updated", website: "shopify.com", time: "1 hour ago", status: "success" },
                    { action: "Critical issue detected", website: "example-site.com", time: "2 hours ago", status: "warning" },
                  ].map((activity, index) => (
                    <div key={index} className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted/30 transition-colors">
                      <div className={`w-2 h-2 rounded-full ${
                        activity.status === 'success' ? 'bg-green-500' :
                        activity.status === 'processing' ? 'bg-blue-500 animate-pulse' :
                        'bg-yellow-500'
                      }`}></div>
                      <div className="flex-1">
                        <div className="text-sm font-medium">{activity.action}</div>
                        <div className="text-xs text-muted-foreground">
                          {activity.website} • {activity.time}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-3">
                  <Button variant="outline" className="h-auto p-4 flex flex-col gap-2">
                    <Search className="w-6 h-6" />
                    <span className="text-sm">Analyze Website</span>
                  </Button>
                  <Button variant="outline" className="h-auto p-4 flex flex-col gap-2">
                    <Target className="w-6 h-6" />
                    <span className="text-sm">Generate Report</span>
                  </Button>
                  <Button variant="outline" className="h-auto p-4 flex flex-col gap-2">
                    <Users className="w-6 h-6" />
                    <span className="text-sm">Competitor Analysis</span>
                  </Button>
                  <Button variant="outline" className="h-auto p-4 flex flex-col gap-2">
                    <Settings className="w-6 h-6" />
                    <span className="text-sm">Configure Alerts</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </div>
  );
}