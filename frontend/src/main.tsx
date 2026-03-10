import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ThemeProvider, CssBaseline } from "@mui/material";
import { RouterProvider } from "react-router-dom";
import { SnackbarProvider } from "notistack";

import "@/index.css";
import { router } from "@/router";
import { theme } from "@/theme/theme";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <SnackbarProvider
        maxSnack={3}
        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
        autoHideDuration={3000}
      >
        <RouterProvider router={router} />
      </SnackbarProvider>
    </ThemeProvider>
  </StrictMode>
);
