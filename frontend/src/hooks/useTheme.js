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
          main: isDark ? '#3b82f6' : '#1976d2',
          light: isDark ? '#60a5fa' : '#42a5f5',
          dark: isDark ? '#1e3a8a' : '#1565c0',
          contrastText: '#ffffff',
        },
        secondary: {
          main: isDark ? '#06b6d4' : '#9c27b0',
          light: isDark ? '#22d3ee' : '#ba68c8',
          dark: isDark ? '#0e7490' : '#7b1fa2',
          contrastText: '#ffffff',
        },
        background: {
          default: isDark ? '#0f1419' : '#fafafa',
          paper: isDark ? 'rgba(42, 45, 58, 0.8)' : '#ffffff',
        },
        text: {
          primary: isDark ? '#e8eaf6' : '#212121',
          secondary: isDark ? '#a5a5a5' : '#757575',
        },
        divider: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.12)',
        action: {
          active: isDark ? '#60a5fa' : '#1976d2',
          hover: isDark ? 'rgba(59, 130, 246, 0.08)' : 'rgba(25, 118, 210, 0.04)',
          selected: isDark ? 'rgba(59, 130, 246, 0.16)' : 'rgba(25, 118, 210, 0.08)',
        },
      },
      typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
        h5: {
          fontWeight: 600,
          letterSpacing: '-0.5px',
        },
        h6: {
          fontWeight: 600,
          letterSpacing: '-0.5px',
        },
        body1: {
          fontFamily: '"Inter", "Roboto", sans-serif',
        },
        body2: {
          fontFamily: '"Inter", "Roboto", sans-serif',
        },
      },
      shape: {
        borderRadius: 12,
      },
      shadows: isDark ? [
        'none',
        '0px 2px 1px -1px rgba(0,0,0,0.2),0px 1px 1px 0px rgba(0,0,0,0.14),0px 1px 3px 0px rgba(0,0,0,0.12)',
        '0px 3px 1px -2px rgba(0,0,0,0.2),0px 2px 2px 0px rgba(0,0,0,0.14),0px 1px 5px 0px rgba(0,0,0,0.12)',
        '0px 3px 3px -2px rgba(0,0,0,0.2),0px 3px 4px 0px rgba(0,0,0,0.14),0px 1px 8px 0px rgba(0,0,0,0.12)',
        '0px 2px 4px -1px rgba(0,0,0,0.2),0px 4px 5px 0px rgba(0,0,0,0.14),0px 1px 10px 0px rgba(0,0,0,0.12)',
        '0px 3px 5px -1px rgba(0,0,0,0.2),0px 5px 8px 0px rgba(0,0,0,0.14),0px 1px 14px 0px rgba(0,0,0,0.12)',
        '0px 3px 5px -1px rgba(0,0,0,0.2),0px 6px 10px 0px rgba(0,0,0,0.14),0px 1px 18px 0px rgba(0,0,0,0.12)',
        '0px 4px 5px -2px rgba(0,0,0,0.2),0px 7px 10px 1px rgba(0,0,0,0.14),0px 2px 16px 1px rgba(0,0,0,0.12)',
        '0px 5px 5px -3px rgba(0,0,0,0.2),0px 8px 10px 1px rgba(0,0,0,0.14),0px 3px 14px 2px rgba(0,0,0,0.12)',
        '0px 5px 6px -3px rgba(0,0,0,0.2),0px 9px 12px 1px rgba(0,0,0,0.14),0px 3px 16px 2px rgba(0,0,0,0.12)',
        '0px 6px 6px -3px rgba(0,0,0,0.2),0px 10px 14px 1px rgba(0,0,0,0.14),0px 4px 18px 3px rgba(0,0,0,0.12)',
        '0px 6px 7px -4px rgba(0,0,0,0.2),0px 11px 15px 1px rgba(0,0,0,0.14),0px 4px 20px 3px rgba(0,0,0,0.12)',
        '0px 7px 8px -4px rgba(0,0,0,0.2),0px 12px 17px 2px rgba(0,0,0,0.14),0px 5px 22px 4px rgba(0,0,0,0.12)',
        '0px 7px 8px -4px rgba(0,0,0,0.2),0px 13px 19px 2px rgba(0,0,0,0.14),0px 5px 24px 4px rgba(0,0,0,0.12)',
        '0px 7px 9px -4px rgba(0,0,0,0.2),0px 14px 21px 2px rgba(0,0,0,0.14),0px 5px 26px 4px rgba(0,0,0,0.12)',
        '0px 8px 9px -5px rgba(0,0,0,0.2),0px 15px 22px 2px rgba(0,0,0,0.14),0px 6px 28px 5px rgba(0,0,0,0.12)',
        '0px 8px 10px -5px rgba(0,0,0,0.2),0px 16px 24px 2px rgba(0,0,0,0.14),0px 6px 30px 5px rgba(0,0,0,0.12)',
        '0px 8px 11px -5px rgba(0,0,0,0.2),0px 17px 26px 2px rgba(0,0,0,0.14),0px 6px 32px 5px rgba(0,0,0,0.12)',
        '0px 9px 11px -5px rgba(0,0,0,0.2),0px 18px 28px 2px rgba(0,0,0,0.14),0px 7px 34px 6px rgba(0,0,0,0.12)',
        '0px 9px 12px -6px rgba(0,0,0,0.2),0px 19px 29px 2px rgba(0,0,0,0.14),0px 7px 36px 6px rgba(0,0,0,0.12)',
        '0px 10px 13px -6px rgba(0,0,0,0.2),0px 20px 31px 3px rgba(0,0,0,0.14),0px 8px 38px 7px rgba(0,0,0,0.12)',
        '0px 10px 13px -6px rgba(0,0,0,0.2),0px 21px 33px 3px rgba(0,0,0,0.14),0px 8px 40px 7px rgba(0,0,0,0.12)',
        '0px 10px 14px -6px rgba(0,0,0,0.2),0px 22px 35px 3px rgba(0,0,0,0.14),0px 8px 42px 7px rgba(0,0,0,0.12)',
        '0px 11px 14px -7px rgba(0,0,0,0.2),0px 23px 36px 3px rgba(0,0,0,0.14),0px 9px 44px 8px rgba(0,0,0,0.12)',
        '0px 11px 15px -7px rgba(0,0,0,0.2),0px 24px 38px 3px rgba(0,0,0,0.14),0px 9px 46px 8px rgba(0,0,0,0.12)',
        '0px 12px 16px -8px rgba(0,0,0,0.2),0px 25px 40px 3px rgba(0,0,0,0.14),0px 10px 48px 9px rgba(0,0,0,0.12)',
        '0px 12px 17px -8px rgba(0,0,0,0.2),0px 26px 42px 3px rgba(0,0,0,0.14),0px 10px 50px 9px rgba(0,0,0,0.12)',
      ] : undefined,
      components: {
        MuiButton: {
          styleOverrides: {
            root: {
              textTransform: 'none',
              fontWeight: 500,
              borderRadius: 8,
              transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
            },
          },
        },
        MuiPaper: {
          styleOverrides: {
            root: {
              backgroundImage: 'none',
            },
          },
        },
        MuiAppBar: {
          styleOverrides: {
            root: {
              backgroundImage: 'none',
            },
          },
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