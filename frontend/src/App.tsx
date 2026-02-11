import { Outlet } from "react-router-dom";
import Navigation from "./components/Navigation";
import { Box } from "@mui/material";

export default function App() {
  return (
    <Box sx={{ display: "flex" }}>
      <Navigation />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
}
