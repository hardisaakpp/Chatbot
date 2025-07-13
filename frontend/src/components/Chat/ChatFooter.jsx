import React from 'react';
import {
  Box,
  Button,
  Typography
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

export const ChatFooter = ({ onClearChat, messageCount, isLoading }) => {
  return (
    <Box sx={{ 
      p: 2, 
      display: 'flex', 
      justifyContent: 'space-between', 
      alignItems: 'center', 
      bgcolor: 'background.default', 
      borderBottomLeftRadius: 12, 
      borderBottomRightRadius: 12 
    }}>
      <Button
        variant="contained"
        color="error"
        size="small"
        startIcon={<DeleteIcon />}
        onClick={onClearChat}
        disabled={isLoading}
      >
        Limpiar chat
      </Button>
      <Typography variant="body2">
        {messageCount} mensajes
      </Typography>
    </Box>
  );
}; 