import "@mui/material/styles";

declare module "@mui/material/styles" {
  interface Palette {
    sidebar: {
      main: string;
      contrastText: string;
    };
  }

  interface PaletteOptions {
    sidebar?: {
      main?: string;
      contrastText?: string;
    };
  }
}