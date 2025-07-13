import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Badge,
  Tooltip,
  Box
} from '@mui/material';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import SettingsBrightnessIcon from '@mui/icons-material/SettingsBrightness';
import WifiIcon from '@mui/icons-material/Wifi';

export const Header = ({ onToggleDarkMode, darkModeIcon, darkModeLabel }) => {
  const getIcon = () => {
    switch (darkModeIcon) {
      case 'system':
        return <SettingsBrightnessIcon />;
      case 'light':
        return <Brightness7Icon />;
      case 'dark':
        return <Brightness4Icon />;
      default:
        return <SettingsBrightnessIcon />;
    }
  };

  return (
    <AppBar 
      position="static" 
      color="primary"
      sx={{
        background: 'linear-gradient(135deg, rgba(15, 20, 25, 0.95) 0%, rgba(26, 31, 46, 0.95) 100%)',
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
        boxShadow: '0 4px 20px 0 rgba(0, 0, 0, 0.3), 0 2px 8px 0 rgba(255, 255, 255, 0.05)',
      }}
    >
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
          <SmartToyIcon 
            sx={{ 
              mr: 1, 
              fontSize: 28,
              animation: 'pulse 2s ease-in-out infinite'
            }} 
          />
          <Typography 
            variant="h6" 
            sx={{ 
              flexGrow: 1,
              fontWeight: 600,
              letterSpacing: '-0.5px',
              background: 'linear-gradient(135deg, #60a5fa 0%, #22d3ee 50%, #a855f7 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundSize: '200% 200%',
              animation: 'gradientText 3s ease infinite'
            }}
          >
            Chatbot de Asistencia Académica
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Tooltip title={darkModeLabel}>
            <IconButton 
              color="inherit" 
              onClick={onToggleDarkMode}
              sx={{
                position: 'relative',
                overflow: 'hidden',
                '&:hover': {
                  transform: 'scale(1.1)',
                }
              }}
            >
              {getIcon()}
            </IconButton>
          </Tooltip>
          
          <Badge 
            color="success" 
            variant="dot" 
            sx={{ 
              ml: 2,
              '& .MuiBadge-dot': {
                backgroundColor: '#10b981',
                animation: 'pulse 2s ease-in-out infinite'
              }
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <WifiIcon sx={{ fontSize: 16, color: '#10b981' }} />
              <Typography variant="body2" sx={{ color: 'inherit' }}>
                En línea
              </Typography>
            </Box>
          </Badge>
        </Box>
      </Toolbar>
    </AppBar>
  );
}; 