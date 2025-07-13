import React, { useRef } from 'react';
import {
  Box,
  Typography,
  Avatar,
  Tooltip,
  Stack,
  Button
} from '@mui/material';
import { TransitionGroup, CSSTransition } from 'react-transition-group';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import SchoolIcon from '@mui/icons-material/School';

export const MessageList = ({ messages, chatEndRef, onCategoryClick }) => {
  const nodeRefs = useRef([]);

  return (
    <Box sx={{ p: 3, minHeight: 320, maxHeight: 400, overflowY: 'auto', bgcolor: 'background.paper' }}>
      <Box textAlign="center" mb={3}>
        <SchoolIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
        <Typography variant="h5" gutterBottom>
          ¡Hola! Soy tu asistente académico
        </Typography>
        <Typography variant="body1">
          Puedo ayudarte con preguntas sobre diversos temas. ¿En qué puedo asistirte hoy?
        </Typography>
      </Box>
      <TransitionGroup component={Stack} spacing={1}>
        {messages.map((msg, idx) => {
          if (!nodeRefs.current[idx]) {
            nodeRefs.current[idx] = React.createRef();
          }
          // Si el mensaje es de tipo categorías, mostrar botones
          if (msg.type === 'categories' && Array.isArray(msg.categories)) {
            return (
              <CSSTransition
                key={idx}
                timeout={500}
                classNames="fade-message"
                nodeRef={nodeRefs.current[idx]}
              >
                <Box ref={nodeRefs.current[idx]} display="flex" flexDirection="column" alignItems="flex-start" mb={2}>
                  <Tooltip title="Bot">
                    <Avatar sx={{ bgcolor: 'primary.main', mr: 1, width: 32, height: 32 }}>
                      <SmartToyIcon fontSize="small" />
                    </Avatar>
                  </Tooltip>
                  <Typography variant="body1" sx={{ mb: 1 }}>{msg.text}</Typography>
                  <Stack direction="row" spacing={1} flexWrap="wrap">
                    {msg.categories.map(cat => (
                      <Button
                        key={cat.id}
                        variant="outlined"
                        size="small"
                        sx={{ mb: 1 }}
                        onClick={() => onCategoryClick(cat.id, cat.name)}
                      >
                        {cat.name}
                      </Button>
                    ))}
                  </Stack>
                </Box>
              </CSSTransition>
            );
          }
          // Mensaje normal
          return (
            <CSSTransition
              key={idx}
              timeout={500}
              classNames="fade-message"
              nodeRef={nodeRefs.current[idx]}
            >
              <Box
                ref={nodeRefs.current[idx]}
                display="flex"
                justifyContent={msg.from === 'user' ? 'flex-end' : 'flex-start'}
                alignItems="flex-end"
              >
                {msg.from === 'bot' && (
                  <Tooltip title="Bot">
                    <Avatar sx={{ bgcolor: 'primary.main', mr: 1, width: 32, height: 32 }}>
                      <SmartToyIcon fontSize="small" />
                    </Avatar>
                  </Tooltip>
                )}
                <span className={`bubble ${msg.from}`}>{msg.text}</span>
                {msg.from === 'user' && (
                  <Tooltip title="Tú">
                    <Avatar sx={{ bgcolor: 'secondary.main', ml: 1, width: 32, height: 32 }}>
                      U
                    </Avatar>
                  </Tooltip>
                )}
              </Box>
            </CSSTransition>
          );
        })}
      </TransitionGroup>
      <div ref={chatEndRef} />
    </Box>
  );
}; 