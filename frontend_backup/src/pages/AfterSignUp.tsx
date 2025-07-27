import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { X, ArrowRight } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface GEONDemoFormProps {
  isOpen: boolean;
  onClose: () => void;
}

const AfterSignUp = ({ isOpen, onClose }: GEONDemoFormProps) => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    organisationName: "",
    contactName: "",
    businessEmail: "",
    businessWebsite: "",
    industry: "",
    teamSize: "",
    useCase: "",
    message: ""
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    toast({
      title: "Demo Request Submitted!",
      description: "We'll be in touch with you shortly to schedule your GEON demo.",
    });
    onClose();
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="relative w-full max-w-2xl bg-gradient-to-br from-primary/20 via-primary/10 to-secondary/20 backdrop-blur-xl border border-primary/20 rounded-2xl shadow-2xl">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-full hover:bg-white/10 transition-colors"
        >
          <X className="w-5 h-5 text-muted-foreground" />
        </button>
        
        <div className="p-8">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <div className="w-12 h-12 bg-gradient-to-r from-primary to-secondary rounded-xl flex items-center justify-center">
                <span className="text-xl font-bold text-white">G</span>
              </div>
            </div>
            <h2 className="text-3xl font-bold text-foreground mb-2">Get a Demo</h2>
            <p className="text-muted-foreground">
              Interested in trying GEON? Fill out this form and we'll be in touch with you.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="organisationName" className="text-foreground font-medium">
                  Organisation Name
                </Label>
                <Input
                  id="organisationName"
                  placeholder="Enter your organisation name"
                  value={formData.organisationName}
                  onChange={(e) => handleInputChange("organisationName", e.target.value)}
                  className="bg-background/50 border-border/50 backdrop-blur-sm"
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="contactName" className="text-foreground font-medium">
                  Contact Name
                </Label>
                <Input
                  id="contactName"
                  placeholder="Enter your full name"
                  value={formData.contactName}
                  onChange={(e) => handleInputChange("contactName", e.target.value)}
                  className="bg-background/50 border-border/50 backdrop-blur-sm"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="businessWebsite" className="text-foreground font-medium">
                  Business Website
                </Label>
                <Input
                  id="businessWebsite"
                  type="url"
                  placeholder="Enter your company website"
                  value={formData.businessWebsite}
                  onChange={(e) => handleInputChange("businessWebsite", e.target.value)}
                  className="bg-background/50 border-border/50 backdrop-blur-sm"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="businessEmail" className="text-foreground font-medium">
                  Business Email
                </Label>
                <Input
                  id="businessEmail"
                  type="email"
                  placeholder="Enter your business email"
                  value={formData.businessEmail}
                  onChange={(e) => handleInputChange("businessEmail", e.target.value)}
                  className="bg-background/50 border-border/50 backdrop-blur-sm"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="industry" className="text-foreground font-medium">
                  Industry/Domain
                </Label>
                <Select onValueChange={(value) => handleInputChange("industry", value)}>
                  <SelectTrigger className="bg-background/50 border-border/50 backdrop-blur-sm">
                    <SelectValue placeholder="Select your industry" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="technology">Technology</SelectItem>
                    <SelectItem value="healthcare">Healthcare</SelectItem>
                    <SelectItem value="finance">Finance & Banking</SelectItem>
                    <SelectItem value="retail">Retail & E-commerce</SelectItem>
                    <SelectItem value="manufacturing">Manufacturing</SelectItem>
                    <SelectItem value="education">Education</SelectItem>
                    <SelectItem value="government">Government</SelectItem>
                    <SelectItem value="media">Media & Entertainment</SelectItem>
                    <SelectItem value="logistics">Logistics & Supply Chain</SelectItem>
                    <SelectItem value="energy">Energy & Utilities</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="teamSize" className="text-foreground font-medium">
                  Team Size
                </Label>
                <Select onValueChange={(value) => handleInputChange("teamSize", value)}>
                  <SelectTrigger className="bg-background/50 border-border/50 backdrop-blur-sm">
                    <SelectValue placeholder="Select team size" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1-10">1-10 employees</SelectItem>
                    <SelectItem value="11-50">11-50 employees</SelectItem>
                    <SelectItem value="51-200">51-200 employees</SelectItem>
                    <SelectItem value="201-500">201-500 employees</SelectItem>
                    <SelectItem value="501-1000">501-1000 employees</SelectItem>
                    <SelectItem value="1000+">1000+ employees</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="useCase" className="text-foreground font-medium">
                Primary Use Case
              </Label>
              <Select onValueChange={(value) => handleInputChange("useCase", value)}>
                <SelectTrigger className="bg-background/50 border-border/50 backdrop-blur-sm">
                  <SelectValue placeholder="What will you primarily use GEON for?" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="analytics">Data Analytics & Insights</SelectItem>
                  <SelectItem value="automation">Process Automation</SelectItem>
                  <SelectItem value="optimization">Performance Optimization</SelectItem>
                  <SelectItem value="monitoring">System Monitoring</SelectItem>
                  <SelectItem value="reporting">Business Reporting</SelectItem>
                  <SelectItem value="integration">System Integration</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="message" className="text-foreground font-medium">
                Tell us more!
              </Label>
              <Textarea
                id="message"
                placeholder="Tell us about your specific requirements, challenges, or anything else you'd like us to know..."
                value={formData.message}
                onChange={(e) => handleInputChange("message", e.target.value)}
                className="bg-background/50 border-border/50 backdrop-blur-sm min-h-[100px] resize-none"
                rows={4}
              />
            </div>

            <Button 
              type="submit" 
              className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-semibold py-3 rounded-xl group transition-all duration-200"
            >
              Submit Request
              <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AfterSignUp;