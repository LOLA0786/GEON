import { Card, CardContent } from "@/components/ui/card";
import { TrendingUp, TrendingDown } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string;
  trend: number;
  trendDirection: "up" | "down";
  icon: React.ReactNode;
}

export function MetricCard({ title, value, trend, trendDirection, icon }: MetricCardProps) {
  const TrendIcon = trendDirection === "up" ? TrendingUp : TrendingDown;
  const trendClass = trendDirection === "up" ? "metric-trend positive" : "metric-trend negative";

  return (
    <Card className="metric-card hover:glow-effect transition-all duration-300">
      <CardContent className="p-6">
        <div className="metric-card-header">
          <div className="flex items-center gap-2">
            {icon}
            <span className="text-sm font-medium text-muted-foreground">{title}</span>
          </div>
        </div>
        <div className="space-y-2">
          <div className="metric-value">{value}</div>
          <div className={trendClass}>
            <TrendIcon className="w-4 h-4" />
            {trend}%
          </div>
        </div>
      </CardContent>
    </Card>
  );
}