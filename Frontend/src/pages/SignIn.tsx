import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Link } from "react-router-dom";
import { Github, Mail, Eye, EyeOff } from "lucide-react";
import { useState } from "react";
import toast from "react-hot-toast";

const SignIn = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };
  const handleSignIn = async (e) => {
     e.preventDefault();
    const validationErrors = validate();
    setErrors(validationErrors);
    if (Object.keys(validationErrors).length == 1) {
    const firstError = Object.values(validationErrors)[0];
    toast.error(firstError);
    return;
    }
    if (Object.keys(validationErrors).length > 1) {
      toast.error("Please fill the the form correctly");
      return;
    }
    try {
      const res = await fetch("http://localhost:8000/auth/signin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });
      if (res.ok) {
        toast.success("Signed in successfully !");
        // navigate("/about");
      } else {
        const errorData = await res.json();
        let message = "Signin failed";
        const detail = errorData?.detail;
        if (typeof detail === "string") {
          message = detail;
        } else if (Array.isArray(detail) && detail.length > 0 && detail[0].msg) {
          message = detail[0].msg;
        }
        toast.error(message);
      }
    } catch (err) {
      toast.error("Network error");
      console.log(err);
    }
  };

   const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  type Errors = {
    firstName?: string;
    lastName?: string;
    email?: string;
    password?: string;
    confirmPassword?: string;
  };

  const validate = () => {
    const newErrors: Errors = {};
    if (!email.trim()) newErrors.email = "Email is required";
    else if (!emailRegex.test(email)) newErrors.email = "Invalid email address";
    if (!password) newErrors.password = "Password is required";
    return newErrors;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center p-4">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-primary/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="w-full max-w-md relative z-10"
      >
        {/* Logo/Brand */}
        {/* <motion.div variants={itemVariants} className="text-center mb-8">
          <Link to="/">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              GEOscore
            </h1>
          </Link>
          <p className="text-muted-foreground mt-2">AI-powered Website Optimization</p>
        </motion.div> */}

        <motion.div variants={itemVariants}>
          <Card className="border-border/50 backdrop-blur-sm bg-card/95 shadow-2xl">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl">Welcome Back</CardTitle>
              <CardDescription>
                Sign in to your account to continue optimizing
              </CardDescription>
            </CardHeader>
            
            <CardContent className="space-y-6">
              {/* Social Sign In */}
              <div className="space-y-3">
                <Button
                  variant="outline"
                  className="w-full h-10 border-border/50 hover:border-primary/50 transition-all duration-300"
                  onClick={() => {
                    // Placeholder for Google sign-in
                    console.log("Google sign-in clicked");
                  }}
                >
                 <img src="google.svg" className="size-4 mr-2"/>
                  Continue with Google
                </Button>

                {/* <Button
                  variant="outline"
                  className="w-full h-10 border-border/50 hover:border-primary/50 transition-all duration-300"
                  onClick={() => {
                    // Placeholder for GitHub sign-in
                    console.log("GitHub sign-in clicked");
                  }}
                >
                  <Github className="w-5 h-5 mr-2" />
                  Continue with GitHub
                </Button>*/}
              </div> 

              <div className="relative">
                <Separator />
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="bg-card px-2 text-muted-foreground text-sm">or</span>
                </div>
              </div>

              {/* Email Sign In Form */}
              <form className="space-y-2">
                <div className="space-y-1">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="enter@example.com"
                    className="h-10"
                    value={email}
                    onChange={(e)=>setEmail(e.target.value)}
                    required
                  />
                </div>

                <div className="space-y-1">
                  <Label htmlFor="password">Password</Label>
                  <div className="relative">
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Enter your password"
                      className="h-10 pr-10"
                      value={password}
                      onChange={(e)=>setPassword(e.target.value)}
                      required
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm">
                  <label className="flex items-center space-x-2 cursor-pointer">
                    <input type="checkbox" className="rounded border-border" />
                    <span className="text-muted-foreground">Remember me</span>
                  </label>
                  <Link to="/forgot-password" className="text-primary hover:text-primary/80 transition-colors">
                    Forgot password?
                  </Link>
                </div>

                <Button
                  type="submit"
                  className="w-full h-10 bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 transition-all duration-300"
                  onClick={handleSignIn}
                >
                  Sign In
                </Button>
              </form>

              <div className="text-center text-sm text-muted-foreground">
                Don't have an account?{" "}
                <Link to="/signup" className="text-primary hover:text-primary/80 font-medium transition-colors">
                  Sign up
                </Link>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div variants={itemVariants} className="text-center mt-6 text-xs text-muted-foreground">
          By signing in, you agree to our{" "}
          <Link to="/terms" className="text-primary hover:text-primary/80">Terms of Service</Link>
          {" "}and{" "}
          <Link to="/privacy" className="text-primary hover:text-primary/80">Privacy Policy</Link>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default SignIn;