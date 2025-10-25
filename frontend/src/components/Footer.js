import React from "react";
import { Box, Typography, IconButton, Link } from "@mui/material";
import GitHubIcon from "@mui/icons-material/GitHub";
import EmailIcon from "@mui/icons-material/Email";

const Footer = () => {
  return (
    <Box
      sx={{
        width: "100%",
        py: 2,
        px: { xs: 2, md: 6 },
        mt: 6,
        borderTop: "1px solid #f0f0f0",
        background: "#f8f9fa",
        position: "relative",
        minHeight: 70,
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-end",
      }}
      component="footer"
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "flex-start",
          justifyContent: "space-between",
          width: "100%",
        }}
      >
        <Typography
          color="textSecondary"
          sx={{ fontSize: "1rem", mb: 1, mt: 0.5 }}
        >
          © 2025 RADS . All rights reserved.
        </Typography>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          <IconButton
            component={Link}
            href="https://github.com/anuragthippani"
            target="_blank"
            rel="noopener"
            aria-label="GitHub"
            size="large"
            sx={{ color: "#616161" }}
          >
            <GitHubIcon />
          </IconButton>
          <IconButton
            component={Link}
            href="mailto:anuragthippani@gmail.com"
            aria-label="Email"
            size="large"
            sx={{ color: "#616161" }}
          >
            <EmailIcon />
          </IconButton>
        </Box>
      </Box>
      <Box
        sx={{
          width: "100%",
          display: "flex",
          justifyContent: "center",
          mt: 0.5,
        }}
      >
        <Typography color="textSecondary" sx={{ fontSize: "1rem" }}>
          Made with <span style={{ color: "#e57373", fontWeight: 700 }}>♥</span>{" "}
          by Anurag Thippani
        </Typography>
      </Box>
    </Box>
  );
};

export default Footer;
