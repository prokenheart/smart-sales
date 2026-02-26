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

const menuItemSx = {
  borderRadius: "8px",
  "&.Mui-selected": {
    backgroundColor: "#1976d2",
    color: "white",
    boxShadow: "0px 4px 8px rgba(0,0,0,0.2)",
  },
  "&.Mui-selected:hover": {
    backgroundColor: "#1565c0",
  },
};

const menuItems = [
  {
    label: "Dashboard",
    path: "/",
    icon: <MdOutlineDashboard size={22} />,
    isActive: (pathname: string) => pathname === "/",
  },
  {
    label: "Orders",
    path: "/orders",
    icon: <MdOutlineShoppingCart size={22} />,
    isActive: (pathname: string) => pathname.startsWith("/orders"),
  },
];

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
        {menuItems.map((item) => (
          <ListItemButton
            key={item.path}
            component={Link}
            to={item.path}
            selected={item.isActive(location.pathname)}
            sx={menuItemSx}
          >
            <ListItemIcon sx={{ minWidth: 35, color: "inherit" }}>
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
};

export default Navigation;
