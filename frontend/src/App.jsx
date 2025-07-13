import React, { useState, useRef, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Paper,
  Button,
  TextField,
  IconButton,
  Badge,
  Stack,
  Container,
  Divider,
  Avatar,
  Tooltip
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import DeleteIcon from '@mui/icons-material/Delete';
import ListIcon from '@mui/icons-material/List';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import CalculateIcon from '@mui/icons-material/Calculate';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import SchoolIcon from '@mui/icons-material/School';

function App() {
  const [messages, setMessages] = useState([
    {
      from: 'bot',
      text: '¡Hola! Soy tu asistente académico',
    },
    {
      from: 'bot',
      text: 'Puedo ayudarte con preguntas sobre diversos temas. ¿En qué puedo asistirte hoy?',
    },
  ]);
  const [input, setInput] = useState('');
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleSend = () => {
    if (input.trim() === '') return;
    setMessages([...messages, { from: 'user', text: input }]);
    setInput('');
    // Aquí luego se conectará con el backend Flask
  };

  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter') handleSend();
  };

  const askQuestion = (question) => {
    setMessages([...messages, { from: 'user', text: question }]);
    // Aquí luego se conectará con el backend Flask
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <Box sx={{ bgcolor: '#f5f5f5', minHeight: '100vh' }}>
      <AppBar position="static" color="primary">
        <Toolbar>
          <SmartToyIcon sx={{ mr: 1 }} />
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Chatbot de Asistencia Académica
          </Typography>
          <Badge color="success" variant="dot" sx={{ mr: 2 }}>
            <Typography variant="body2">En línea</Typography>
          </Badge>
        </Toolbar>
      </AppBar>
      <Container maxWidth="sm" sx={{ py: 5 }}>
        <Paper elevation={4} sx={{ p: 0, borderRadius: 3 }}>
          <Box sx={{ p: 3, minHeight: 320, maxHeight: 400, overflowY: 'auto', bgcolor: '#fafafa' }}>
            <Box textAlign="center" mb={3}>
              <SchoolIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h5" gutterBottom>
                ¡Hola! Soy tu asistente académico
              </Typography>
              <Typography variant="body1">
                Puedo ayudarte con preguntas sobre diversos temas. ¿En qué puedo asistirte hoy?
              </Typography>
            </Box>
            <Stack spacing={1}>
              {messages.map((msg, idx) => (
                <Box
                  key={idx}
                  display="flex"
                  justifyContent={msg.from === 'user' ? 'flex-end' : 'flex-start'}
                >
                  {msg.from === 'bot' && (
                    <Tooltip title="Bot">
                      <Avatar sx={{ bgcolor: 'primary.main', mr: 1, width: 32, height: 32 }}>
                        <SmartToyIcon fontSize="small" />
                      </Avatar>
                    </Tooltip>
                  )}
                  <Box
                    sx={{
                      bgcolor: msg.from === 'user' ? 'primary.main' : 'grey.300',
                      color: msg.from === 'user' ? 'white' : 'black',
                      px: 2,
                      py: 1,
                      borderRadius: 2,
                      maxWidth: '75%',
                      wordBreak: 'break-word',
                    }}
                  >
                    {msg.text}
                  </Box>
                  {msg.from === 'user' && (
                    <Tooltip title="Tú">
                      <Avatar sx={{ bgcolor: 'secondary.main', ml: 1, width: 32, height: 32 }}>
                        U
                      </Avatar>
                    </Tooltip>
                  )}
                </Box>
              ))}
              <div ref={chatEndRef} />
            </Stack>
          </Box>
          <Divider />
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1, p: 2, flexWrap: 'wrap' }}>
            <Button
              variant="outlined"
              startIcon={<ListIcon />}
              onClick={() => askQuestion('¿Cuáles son los temas disponibles?')}
            >
              Temas disponibles
            </Button>
            <Button
              variant="outlined"
              startIcon={<HelpOutlineIcon />}
              onClick={() => askQuestion('¿Cómo funciona este chatbot?')}
            >
              ¿Cómo funciona?
            </Button>
            <Button
              variant="outlined"
              startIcon={<CalculateIcon />}
              onClick={() => askQuestion('¿Puedes ayudarme con matemáticas?')}
            >
              Matemáticas
            </Button>
          </Box>
          <Divider />
          <Box sx={{ p: 2, display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Escribe tu pregunta aquí..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleInputKeyDown}
              size="small"
            />
            <IconButton color="primary" onClick={handleSend} sx={{ height: 40, width: 40 }}>
              <SendIcon />
            </IconButton>
          </Box>
          <Divider />
          <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center', bgcolor: '#f5f5f5', borderBottomLeftRadius: 12, borderBottomRightRadius: 12 }}>
            <Button
              variant="contained"
              color="error"
              size="small"
              startIcon={<DeleteIcon />}
              onClick={clearChat}
            >
              Limpiar chat
            </Button>
            <Typography variant="body2">
              {messages.length} mensajes
            </Typography>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
}

export default App;
