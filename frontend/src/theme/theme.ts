import { createTheme } from "@mui/material/styles";

const COLORS = {
  primary: "#f9b17a",
  primaryContrast: "#2d3250",
  primaryHover: "#e9a66f",

  secondary: "#2d3250",
  secondaryContrast: "#ffffff",
  secondaryHover: "#1f2436",

  accent: "#676f9d",
  accentContrast: "#ffffff",
  accentHover: "#5b6390",

  background: "#f4f5f7",
  surface: "#ffffff",

  tableHeadBackground: "#eef0f3",
  tableRowHover: "#ffe3cc",

  textPrimary: "#2d3250",
  textSecondary: "#676f9d",
};

export const theme = createTheme({
  palette: {
    mode: "light",

    // Primary = CTA (Add Order, Active pagination)
    primary: {
      main: COLORS.primary,
      contrastText: COLORS.primaryContrast,
    },

    // Secondary
    secondary: {
      main: COLORS.secondary,
      contrastText: COLORS.secondaryContrast,
    },

    background: {
      default: COLORS.background,
      paper: COLORS.surface, // card, table
    },

    text: {
      primary: COLORS.textPrimary,
      secondary: COLORS.textSecondary,
    },
  },

  shape: {
    borderRadius: 12,
  },

  components: {
    // ===== BUTTON =====
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
          fontWeight: 600,
          borderRadius: 10,
        },
        containedPrimary: {
          backgroundColor: COLORS.primary,
          color: COLORS.primaryContrast,
          "&:hover": {
            backgroundColor: COLORS.primaryHover,
          },
        },
        containedSecondary: {
          backgroundColor: COLORS.accent,
          color: COLORS.accentContrast,
          "&:hover": {
            backgroundColor: COLORS.accentHover,
          },
        },
      },
    },

    // ===== TABLE =====

    MuiTableHead: {
      styleOverrides: {
        root: {
          "& .MuiTableCell-head": {
            color: COLORS.textPrimary,
            backgroundColor: COLORS.tableHeadBackground,
            fontWeight: 600,
          },
        },
      },
    },

    MuiTableRow: {
      styleOverrides: {
        root: {
          backgroundColor: COLORS.surface,
          "&.MuiTableRow-hover:hover": {
            backgroundColor: COLORS.tableRowHover,
          },
        },
      },
    },

    MuiTableCell: {
      styleOverrides: {
        root: {
          color: COLORS.textPrimary,
        },
      },
    },

    // ===== INPUT / SEARCH =====
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          backgroundColor: COLORS.surface,
          "& .MuiOutlinedInput-notchedOutline": {
            borderColor: COLORS.accent,
          },
          "&:hover .MuiOutlinedInput-notchedOutline": {
            borderColor: COLORS.primary,
          },
          "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: COLORS.primary,
          },
        },
        input: {
          color: COLORS.textPrimary,
          "&::placeholder": {
            color: COLORS.textSecondary,
            opacity: 0.7,
          },
        },
      },
    },

    // ===== Autocomplete =====

    MuiAutocomplete: {
      styleOverrides: {
        paper: {
          backgroundColor: COLORS.surface,
          color: COLORS.textPrimary,
        },
        listbox: {
          padding: 0,
        },
        option: {
          color: COLORS.textPrimary,
        },
      },
    },
  },
});
