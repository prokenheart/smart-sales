import {
  Drawer,
  List,
  ListItemButton,
  ListItemText,
  ListItemIcon,
} from "@mui/material";
import { Link, useLocation } from "react-router-dom";
import { MdOutlineDashboard, MdOutlineShoppingCart } from "react-icons/md";
import type { ReactElement } from "react";

const drawerWidth = 160;

const Navigation = (): ReactElement => {
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {
          width: drawerWidth,
          boxSizing: "border-box",
          padding: "10px",
        },
      }}
    >
      <List sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
        <ListItemButton
          component={Link}
          to="/"
          selected={location.pathname === "/"}
          sx={{
            borderRadius: "8px",
            "&.Mui-selected": {
              backgroundColor: "#1976d2",
              color: "white",
              boxShadow: "0px 4px 8px rgba(0,0,0,0.2)",
            },
            "&.Mui-selected:hover": {
              backgroundColor: "#1565c0",
            },
          }}
        >
          <ListItemIcon sx={{ minWidth: 35, color: "inherit" }}>
            <MdOutlineDashboard size={22} />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItemButton>

        <ListItemButton
          component={Link}
          to="/orders"
          selected={location.pathname.startsWith("/orders")}
          sx={{
            borderRadius: "8px",
            "&.Mui-selected": {
              backgroundColor: "#1976d2",
              color: "white",
              boxShadow: "0px 4px 8px rgba(0,0,0,0.2)",
            },
            "&.Mui-selected:hover": {
              backgroundColor: "#1565c0",
            },
          }}
        >
          <ListItemIcon sx={{ minWidth: 35, color: "inherit" }}>
            <MdOutlineShoppingCart size={22} />
          </ListItemIcon>
          <ListItemText primary="Orders" />
        </ListItemButton>
      </List>
    </Drawer>
  );
};

export default Navigation;
