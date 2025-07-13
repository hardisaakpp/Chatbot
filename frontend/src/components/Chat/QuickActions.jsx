import React from 'react';
import {
  Box,
  Button
} from '@mui/material';
import ListIcon from '@mui/icons-material/List';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { QUICK_QUESTIONS } from '../../utils/constants';

export const QuickActions = ({ onAskQuestion, isLoading }) => {
  const getIcon = (iconName) => {
    switch (iconName) {
      case 'ListIcon':
        return <ListIcon />;
      case 'HelpOutlineIcon':
        return <HelpOutlineIcon />;
      default:
        return <ListIcon />;
    }
  };

  // Filtrar para mostrar solo los botones de Temas disponibles y ¿Cómo funciona?
  const filteredQuestions = QUICK_QUESTIONS.filter(q =>
    q.text !== 'Matemáticas'
  );

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1, p: 2, flexWrap: 'wrap' }}>
      {filteredQuestions.map((item, index) => (
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