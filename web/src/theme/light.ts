import createTheme from "@mui/material/styles/createTheme";

const lightTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2e5398',
    },
    secondary: {
      main: '#f55e3b',
    },
    warning: {
      main: '#ffe566',
    },
    info: {
      main: '#94c0ff',
    },
    error: {
      main: '#da4a4a',
    },
    success: {
      main: '#92ed94',
    },
  },
});

export default lightTheme;