import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Badge,
  Tooltip
} from '@mui/material';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';

export const Header = ({ onToggleDarkMode, darkModeIcon, darkModeLabel }) => {
  const getIcon = () => {
    switch (darkModeIcon) {
      case 'system':
        return <Brightness4Icon />;
      case 'light':
        return <Brightness7Icon />;
      case 'dark':
        return <Brightness4Icon />;
      default:
        return <Brightness4Icon />;
    }
  };

  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <SmartToyIcon sx={{ mr: 1 }} />
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Chatbot de Asistencia Académica
        </Typography>
        <Tooltip title={darkModeLabel}>
          <IconButton color="inherit" onClick={onToggleDarkMode}>
            {getIcon()}
          </IconButton>
        </Tooltip>
        <Badge color="success" variant="dot" sx={{ ml: 2 }}>
          <Typography variant="body2">En línea</Typography>
        </Badge>
      </Toolbar>
    </AppBar>
  );
}; 