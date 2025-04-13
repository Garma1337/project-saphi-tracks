import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './App.css'
import {HashRouter} from 'react-router-dom'
import {CssBaseline, ThemeProvider} from '@mui/material'
import getCurrentTheme from "./utils/getCurrentTheme.ts";
import darkTheme from "./theme/dark.ts";
import lightTheme from "./theme/light.ts";
import reportWebVitals from "./utils/reportWebVitals.ts";

let theme;
const mode = getCurrentTheme();

if (mode === 'dark') {
    theme = darkTheme;
} else {
    theme = lightTheme;
}

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <HashRouter>
            <ThemeProvider theme={theme}>
                <CssBaseline/>
                <App/>
            </ThemeProvider>
        </HashRouter>
    </React.StrictMode>
)

reportWebVitals();
