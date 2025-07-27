import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Link } from "react-router-dom";
import { Github, Eye, EyeOff, CheckCircle } from "lucide-react";
import { useState } from "react";
import toast from "react-hot-toast";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const SignUp = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();
  const [errors, setErrors] = useState({});


  const handleSignUp = async (e) => {
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
      const res = await fetch("http://localhost:8000/auth/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
          full_name: firstName + " " + lastName,
        }),
      });
      if (res.ok) {
        toast.success("OTP sent successfully!");
        navigate("/about");
      } else {
        const errorData = await res.json();
        let message = "Signup failed";
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
  
  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  const passwordCriteria = [
    { label: "At least 6 characters", met: password.length >= 8 },
    // { label: "Contains uppercase letter", met: /[A-Z]/.test(password) },
    { label: "Contains lowercase letter", met: /[a-z]/.test(password) },
    { label: "Contains number", met: /\d/.test(password) },
  ];
  // Add this inside your SignUp component, after passwordCriteria
  const getPasswordStrength = () => {
    const metCount = passwordCriteria.filter((c) => c.met).length;
    if (password.length === 0) return "";
    if (metCount <= 1) return "Weak";
    if (metCount === 1 || metCount === 2) return "Medium";
    if (metCount === 3) return "Strong";
    return "";
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
    if (!firstName.trim()) newErrors.firstName = "First name is required";
    if (!lastName.trim()) newErrors.lastName = "Last name is required";
    if (!email.trim()) newErrors.email = "Email is required";
    else if (!emailRegex.test(email)) newErrors.email = "Invalid email address";
    if (!password) newErrors.password = "Password is required";
    else if (getPasswordStrength() === "Weak") newErrors.password = "Password is too weak";
    if (!confirmPassword) newErrors.confirmPassword = "Please confirm your password";
    else if (password !== confirmPassword) newErrors.confirmPassword = "Passwords do not match";
    return newErrors;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 flex items-center justify-center p-4">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/3 left-1/3 w-64 h-64 bg-accent/10 rounded-full blur-3xl animate-pulse delay-500" />
        <div className="absolute bottom-1/3 right-1/3 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-pulse delay-1500" />
      </div>

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="w-full max-w-md relative z-10"
      >
        {/* Logo/Brand
        <motion.div variants={itemVariants} className="text-center mb-8">
          <Link to="/">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            <span className="text-white">Welcome to </span> <span>GEON</span>
            </h1>
          </Link>
        </motion.div> */}

        <motion.div variants={itemVariants}>
          <Card className="border-border/50 backdrop-blur-sm bg-card/95 shadow-2xl">
            <CardHeader className="text-center">
              <motion.div variants={itemVariants} className="text-center mb-2">
                <Link to="/">
                  <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                    <span className="text-white">Welcome to </span>{" "}
                    <span>GEON</span>
                  </h1>
                </Link>
              </motion.div>
              <CardDescription>
                Join thousands of developers optimizing their websites
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-6">
              {/* Social Sign Up */}
              <div className="space-y-3">
                <Button
                  variant="outline"
                  className="w-full h-10 border-border/50 hover:border-primary/50 transition-all duration-300"
                  onClick={() => {
                    // Placeholder for Google sign-up
                    console.log("Google sign-up clicked");
                  }}
                >
                  <img src="google.svg" className="size-4 mr-2" />
                  Continue with Google
                </Button>

                {/* <Button
                  variant="outline"
                  className="w-full h-10 border-border/50 hover:border-primary/50 transition-all duration-300"
                  onClick={() => {
                    // Placeholder for GitHub sign-up
                    console.log("GitHub sign-up clicked");
                  }}
                >
                  <Github className="w-5 h-5 mr-2" />
                  Continue with GitHub
                </Button> */}
              </div>

              <div className="relative">
                <Separator />
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="bg-card px-2 text-muted-foreground text-sm">
                    or
                  </span>
                </div>
              </div>

              {/* Email Sign Up Form */}
              <form className="space-y-1">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <Label htmlFor="firstName">First Name</Label>
                    <Input
                      id="firstName"
                      placeholder="John"
                      className="h-10"
                      required
                      value={firstName}
                      onChange={(e) => setFirstName(e.target.value)}
                    />
                  </div>
                  <div className="space-y-1">
                    <Label htmlFor="lastName">Last Name</Label>
                    <Input
                      id="lastName"
                      placeholder="Doe"
                      className="h-10"
                      required
                      value={lastName}
                      onChange={(e) => setLastName(e.target.value)}
                    />
                  </div>
                </div>

                <div className="space-y-1">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="john@example.com"
                    className="h-10"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>

                {/* <div className="space-y-1">
                  <Label htmlFor="password">Password</Label>
                  <div className="relative">
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Create a strong password"
                      className="h-10 pr-10"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
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
                  </div> */}

                {/* Password strength indicator
                  {password && (
                    <div className="mt-2 space-y-1">
                      {passwordCriteria.map((criterion, index) => (
                        <div
                          key={index}
                          className="flex items-center space-x-2 text-xs"
                        >
                          <CheckCircle
                            className={`h-3 w-3 ${
                              criterion.met
                                ? "text-green-500"
                                : "text-muted-foreground"
                            }`}
                          />
                          <span
                            className={
                              criterion.met
                                ? "text-green-500"
                                : "text-muted-foreground"
                            }
                          >
                            {criterion.label}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>*/}
                <div className="space-y-1">
                  <Label htmlFor="password">Password</Label>
                  <div className="relative">
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Create a strong password"
                      className="h-10 pr-10"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
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
                  {/* Password strength indicator */}
                  {password && (
                    <div
                      className="mt-2 text-xs font-semibold"
                      style={{
                        color:
                          getPasswordStrength() === "Strong"
                            ? "#22c55e"
                            : getPasswordStrength() === "Medium"
                            ? "#eab308"
                            : "#ef4444",
                      }}
                    >
                      Password strength: {getPasswordStrength()}
                    </div>
                  )}
                </div>

                <div className="space-y-1">
                  <Label htmlFor="confirmPassword">Confirm Password</Label>
                  <div className="relative">
                    <Input
                      id="confirmPassword"
                      type={showConfirmPassword ? "text" : "password"}
                      placeholder="Confirm your password"
                      className="h-10 pr-10"
                      value={confirmPassword}
                      onChange={(e)=>setConfirmPassword(e.target.value)}
                      required
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                      onClick={() =>
                        setShowConfirmPassword(!showConfirmPassword)
                      }
                    >
                      {showConfirmPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>

                <div className="flex items-center space-x-2 pt-3 pb-1">
                  <input
                    type="checkbox"
                    id="terms"
                    className="rounded border-border"
                    required
                  />
                  <label
                    htmlFor="terms"
                    className="text-sm text-muted-foreground"
                  >
                    I agree to the{" "}
                    <Link
                      to="/terms"
                      className="text-primary hover:text-primary/80"
                    >
                      Terms of Service
                    </Link>{" "}
                    and{" "}
                    <Link
                      to="/privacy"
                      className="text-primary hover:text-primary/80"
                    >
                      Privacy Policy
                    </Link>
                  </label>
                </div>

                <Button
                  type="submit"
                  className="w-full h-11 bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 transition-all duration-300"
                  onClick={handleSignUp}
                >
                  Create Account
                </Button>
              </form>

              <div className="text-center text-sm text-muted-foreground">
                Already have an account?{" "}
                <Link
                  to="/signin"
                  className="text-primary hover:text-primary/80 font-medium transition-colors"
                >
                  Sign in
                </Link>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default SignUp;
