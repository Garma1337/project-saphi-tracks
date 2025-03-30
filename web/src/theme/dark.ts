import {createTheme} from "@mui/material";

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#2e5398',
    },
    secondary: {
      main: '#f55e3b',
    },
    warning: {
      main: '#ffe584',
    },
    info: {
      main: '#aed8ff',
    },
    error: {
      main: '#ffa99a',
    },
    success: {
      main: '#8ce492',
    },
  },
})

export default darkTheme;
