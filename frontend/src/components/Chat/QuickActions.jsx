import React from 'react';
import {
  Box,
  Button
} from '@mui/material';
import ListIcon from '@mui/icons-material/List';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import CalculateIcon from '@mui/icons-material/Calculate';
import { QUICK_QUESTIONS } from '../../utils/constants';

export const QuickActions = ({ onAskQuestion, isLoading }) => {
  const getIcon = (iconName) => {
    switch (iconName) {
      case 'ListIcon':
        return <ListIcon />;
      case 'HelpOutlineIcon':
        return <HelpOutlineIcon />;
      case 'CalculateIcon':
        return <CalculateIcon />;
      default:
        return <ListIcon />;
    }
  };

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1, p: 2, flexWrap: 'wrap' }}>
      {QUICK_QUESTIONS.map((item, index) => (
        <Button
          key={index}
          variant="outlined"
          startIcon={getIcon(item.icon)}
          onClick={() => onAskQuestion(item.question)}
          disabled={isLoading}
        >
          {item.text}
        </Button>
      ))}
    </Box>
  );
}; 