import { useState, useMemo } from 'react';
import { useMediaQuery } from '@mui/material';
import { createTheme } from '@mui/material/styles';

export const useTheme = () => {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const [darkMode, setDarkMode] = useState(null); // null = seguir sistema

  // Determinar el modo actual
  const isDark = darkMode === null ? prefersDarkMode : darkMode;

  const theme = useMemo(() =>
    createTheme({
      palette: {
        mode: isDark ? 'dark' : 'light',
        primary: {
          main: '#1976d2',
        },
        secondary: {
          main: '#9c27b0',
        },
      },
    }), [isDark]);

  const toggleDarkMode = () => {
    if (darkMode === null) {
      setDarkMode(!prefersDarkMode);
    } else if (darkMode === true) {
      setDarkMode(false);
    } else {
      setDarkMode(null); // volver a seguir sistema
    }
  };

  const getDarkModeIcon = () => {
    if (darkMode === null) return 'system'; // sistema
    return isDark ? 'light' : 'dark';
  };

  const getDarkModeLabel = () => {
    if (darkMode === null) return 'Seguir sistema';
    return isDark ? 'Modo claro' : 'Modo oscuro';
  };

  return {
    isDark,
    theme,
    toggleDarkMode,
    getDarkModeIcon,
    getDarkModeLabel
  };
}; 