import React from "react";
import {
  Container,
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Paper,
  Chip,
} from "@mui/material";
import {
  Security,
  Assessment,
  Speed,
  CheckCircle,
  TrendingUp,
  Shield,
  Analytics,
  ArrowForward,
} from "@mui/icons-material";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <Security sx={{ fontSize: 50, color: "#667eea" }} />,
      title: "AI-Powered Detection",
      description:
        "Advanced machine learning algorithms analyze return patterns to detect potential abuse cases with high accuracy.",
    },
    {
      icon: <Assessment sx={{ fontSize: 50, color: "#764ba2" }} />,
      title: "Real-Time Analytics",
      description:
        "Get instant insights into return trends, risk scores, and suspicious activities across your platform.",
    },
    {
      icon: <Speed sx={{ fontSize: 50, color: "#f093fb" }} />,
      title: "Fast Processing",
      description:
        "Process thousands of return requests in seconds with our optimized detection engine.",
    },
    {
      icon: <Shield sx={{ fontSize: 50, color: "#4facfe" }} />,
      title: "Fraud Prevention",
      description:
        "Protect your business from return fraud with comprehensive risk scoring and pattern analysis.",
    },
  ];

  const stats = [
    { label: "Detection Accuracy", value: "95%", icon: <CheckCircle /> },
    { label: "Cases Analyzed", value: "1K+", icon: <TrendingUp /> },
    { label: "Response Time", value: "<2s", icon: <Speed /> },
    { label: "Risk Categories", value: "3", icon: <Analytics /> },
  ];

  return (
    <Box
      sx={{
        minHeight: "calc(100vh - 64px)",
        background: "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
      }}
    >
      {/* Hero Section */}
      <Box
        sx={{
          background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
          color: "white",
          py: 8,
          position: "relative",
          overflow: "hidden",
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={7}>
              <Typography
                variant="h2"
                sx={{
                  fontWeight: 800,
                  mb: 2,
                  textShadow: "2px 2px 4px rgba(0,0,0,0.2)",
                }}
              >
                Return Abuse Detection System
              </Typography>
              <Typography variant="h5" sx={{ mb: 4, opacity: 0.95 }}>
                Protect your business with intelligent fraud detection powered
                by advanced AI and machine learning.
              </Typography>
              <Box sx={{ display: "flex", gap: 2 }}>
                <Button
                  variant="contained"
                  size="large"
                  endIcon={<ArrowForward />}
                  onClick={() => navigate("/dashboard")}
                  sx={{
                    bgcolor: "white",
                    color: "#667eea",
                    px: 4,
                    py: 1.5,
                    fontWeight: 600,
                    "&:hover": {
                      bgcolor: "rgba(255,255,255,0.9)",
                      transform: "translateY(-2px)",
                      boxShadow: "0 8px 20px rgba(0,0,0,0.2)",
                    },
                    transition: "all 0.3s",
                  }}
                >
                  View Dashboard
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  sx={{
                    color: "white",
                    borderColor: "white",
                    px: 4,
                    py: 1.5,
                    fontWeight: 600,
                    "&:hover": {
                      borderColor: "white",
                      bgcolor: "rgba(255,255,255,0.1)",
                    },
                  }}
                >
                  Learn More
                </Button>
              </Box>
            </Grid>
            <Grid item xs={12} md={5}>
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <Security sx={{ fontSize: 250, opacity: 0.2 }} />
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Stats Section */}
      <Container maxWidth="lg" sx={{ mt: -4, position: "relative", zIndex: 1 }}>
        <Grid container spacing={3}>
          {stats.map((stat, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Paper
                elevation={3}
                sx={{
                  p: 3,
                  textAlign: "center",
                  background: "white",
                  borderRadius: 3,
                  transition: "transform 0.3s, box-shadow 0.3s",
                  "&:hover": {
                    transform: "translateY(-8px)",
                    boxShadow: "0 12px 30px rgba(0,0,0,0.15)",
                  },
                }}
              >
                <Box
                  sx={{
                    color: "#667eea",
                    mb: 1,
                    display: "flex",
                    justifyContent: "center",
                  }}
                >
                  {React.cloneElement(stat.icon, { sx: { fontSize: 40 } })}
                </Box>
                <Typography variant="h3" sx={{ fontWeight: 700, mb: 1 }}>
                  {stat.value}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {stat.label}
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography variant="h3" align="center" sx={{ fontWeight: 700, mb: 2 }}>
          Key Features
        </Typography>
        <Typography
          variant="h6"
          align="center"
          color="textSecondary"
          sx={{ mb: 6 }}
        >
          Everything you need to detect and prevent return abuse
        </Typography>
        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={6} key={index}>
              <Card
                elevation={2}
                sx={{
                  height: "100%",
                  borderRadius: 3,
                  transition: "all 0.3s",
                  "&:hover": {
                    transform: "translateY(-8px)",
                    boxShadow: "0 12px 30px rgba(0,0,0,0.1)",
                  },
                }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                  <Typography variant="h5" sx={{ fontWeight: 600, mb: 2 }}>
                    {feature.title}
                  </Typography>
                  <Typography variant="body1" color="textSecondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* CTA Section */}
      <Box
        sx={{
          background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
          py: 8,
          color: "white",
          textAlign: "center",
        }}
      >
        <Container maxWidth="md">
          <Typography variant="h3" sx={{ fontWeight: 700, mb: 2 }}>
            Ready to Get Started?
          </Typography>
          <Typography variant="h6" sx={{ mb: 4, opacity: 0.9 }}>
            Start analyzing return cases and protect your business today
          </Typography>
          <Button
            variant="contained"
            size="large"
            endIcon={<ArrowForward />}
            onClick={() => navigate("/dashboard")}
            sx={{
              bgcolor: "white",
              color: "#667eea",
              px: 6,
              py: 2,
              fontSize: "1.1rem",
              fontWeight: 600,
              "&:hover": {
                bgcolor: "rgba(255,255,255,0.9)",
                transform: "translateY(-2px)",
                boxShadow: "0 8px 20px rgba(0,0,0,0.3)",
              },
              transition: "all 0.3s",
            }}
          >
            Go to Dashboard
          </Button>
        </Container>
      </Box>
    </Box>
  );
};

export default Home;
