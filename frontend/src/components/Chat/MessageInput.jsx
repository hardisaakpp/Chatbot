import React, { useState } from 'react';
import {
  Box,
  TextField,
  IconButton,
  CircularProgress
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

export const MessageInput = ({ onSendMessage, isLoading }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() === '' || isLoading) return;
    onSendMessage(input);
    setInput('');
  };

  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box sx={{ p: 2, display: 'flex', gap: 1 }}>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Escribe tu pregunta aquí..."
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={handleInputKeyDown}
        size="small"
        disabled={isLoading}
      />
      <IconButton 
        color="primary" 
        onClick={handleSend} 
        sx={{ height: 40, width: 40 }}
        disabled={isLoading || input.trim() === ''}
      >
        {isLoading ? <CircularProgress size={20} /> : <SendIcon />}
      </IconButton>
    </Box>
  );
}; 