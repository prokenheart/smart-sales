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

const drawerWidth = 180;

const Navigation = (): ReactElement => {
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
          p: 2,
          backgroundColor: "sidebar.main",
          color: "sidebar.contrastText",
          borderRight: "none",
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
            sx={{
              borderRadius: 2,
              color: "text.main",
              transition: "all 0.2s ease",

              "&:hover": {
                backgroundColor: "rgba(255,255,255,0.08)",
                color: "primary.main",
                transform: "translateX(6px)",
              },

              "&.Mui-selected": {
                backgroundColor: "primary.main",
                color: "primary.contrastText",
                boxShadow: "0px 6px 15px rgba(0,0,0,0.25)",

                "& .MuiListItemIcon-root": {
                  color: "primary.contrastText",
                },
                "&:hover": {
                  backgroundColor: "primary.main",
                  color: "primary.contrastText",
                  transform: "translateX(6px)",
                },
              },
            }}
          >
            <ListItemIcon
              sx={{
                minWidth: 35,
                color: "inherit",
              }}
            >
              {item.icon}
            </ListItemIcon>

            <ListItemText
              primary={item.label}
            />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
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

export default Navigation;