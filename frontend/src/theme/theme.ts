import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    mode: "light",

    // Primary = CTA (Add Order, Active pagination)
    primary: {
      main: "#f9b17a",
      contrastText: "#2d3250",
    },

    // Secondary = UI phụ
    secondary: {
      main: "#2d3250",
      contrastText: "#ffffff",
    },

    background: {
      default: "#f4f5f7",
      paper: "#ffffff", // card, table
    },

    text: {
      primary: "#2d3250",
      secondary: "#676f9d",
    },

    sidebar: {
      main: "#2d3250",
      contrastText: "#ffffff",
    } as any,
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
          backgroundColor: "#f9b17a",
          color: "#2d3250",
          "&:hover": {
            backgroundColor: "#e9a66f",
          },
        },
        containedSecondary: {
          backgroundColor: "#676f9d",
          color: "#ffffff",
          "&:hover": {
            backgroundColor: "#5b6390",
          },
        },
      },
    },

    // ===== TABLE =====


    MuiTableHead: {
      styleOverrides: {
        root: {
          "& .MuiTableCell-head": {
            color: "#2d3250",
            backgroundColor: "#f4f5f7",
            fontWeight: 600,
          },
        },
      },
    },

    MuiTableRow: {
      styleOverrides: {
        root: {
          backgroundColor: "#ffffff",
          "&.MuiTableRow-hover:hover": {
            backgroundColor: "#ffc79c",
          },
        },
      },
    },

    MuiTableCell: {
      styleOverrides: {
        root: {
          color: "#2d3250",
        },
      },
    },

    // ===== INPUT / SEARCH =====
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          backgroundColor: "#ffffff",
          "& .MuiOutlinedInput-notchedOutline": {
            borderColor: "#676f9d",
          },
          "&:hover .MuiOutlinedInput-notchedOutline": {
            borderColor: "#f9b17a",
          },
          "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderColor: "#f9b17a",
          },
        },
        input: {
          color: "#2d3250",
          "&::placeholder": {
            color: "#676f9d",
            opacity: 0.7,
          },
        },
      },
    },

    // ===== PAGINATION =====
    MuiPaginationItem: {
      styleOverrides: {
        root: {
          color: "#ffffff",
          backgroundColor: "#424769",
          "&.Mui-selected": {
            backgroundColor: "#f9b17a",
            color: "#2d3250",
            fontWeight: 600,
          },
          "&:hover": {
            backgroundColor: "#676f9d",
          },
        },
      },
    },

    MuiAutocomplete: {
      styleOverrides: {
        paper: {
          backgroundColor: "#ffffff",
          color: "#2d3250",
        },
        listbox: {
          padding: 0,
        },
        option: {
          color: "#2d3250",
          "&.Mui-focused": {
            backgroundColor: "#ffc79c",
          },
          "&[aria-selected='true']": {
            backgroundColor: "#f9b17a",
            color: "#2d3250",
          },
        },
      },
    },
  },
});
