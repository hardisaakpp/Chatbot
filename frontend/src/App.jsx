import React, { useState, useRef, useEffect, useMemo } from 'react';
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
  Tooltip,
  CssBaseline,
  useMediaQuery,
  Switch
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import SendIcon from '@mui/icons-material/Send';
import DeleteIcon from '@mui/icons-material/Delete';
import ListIcon from '@mui/icons-material/List';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import CalculateIcon from '@mui/icons-material/Calculate';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import SchoolIcon from '@mui/icons-material/School';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { TransitionGroup, CSSTransition } from 'react-transition-group';
import './App.css'; // Para animaciones CSS

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

  // Dark mode: sistema y manual
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

  useEffect(() => {
    // Cambia el atributo data-theme del body para modo oscuro elegante
    document.body.setAttribute('data-theme', isDark ? 'dark' : 'light');
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isDark]);

  const handleSend = () => {
    if (input.trim() === '') return;
    setMessages(prevMessages => [...prevMessages, { from: 'user', text: input }]);
    setInput('');
    // Aquí luego se conectará con el backend Flask
  };

  const handleInputKeyDown = (e) => {
    if (e.key === 'Enter') handleSend();
  };

  const askQuestion = (question) => {
    setMessages(prevMessages => [...prevMessages, { from: 'user', text: question }]);
    // Aquí luego se conectará con el backend Flask
  };

  const clearChat = () => {
    setMessages([
      {
        from: 'bot',
        text: '¡Hola! Soy tu asistente académico',
      },
      {
        from: 'bot',
        text: 'Puedo ayudarte con preguntas sobre diversos temas. ¿En qué puedo asistirte hoy?',
      },
    ]);
  };

  // Alternar dark mode manualmente o seguir sistema
  const handleToggleDarkMode = () => {
    if (darkMode === null) {
      setDarkMode(!prefersDarkMode);
    } else if (darkMode === true) {
      setDarkMode(false);
    } else {
      setDarkMode(null); // volver a seguir sistema
    }
  };

  // Icono y texto para el botón de dark mode
  const getDarkModeIcon = () => {
    if (darkMode === null) return <Brightness4Icon />; // sistema
    return isDark ? <Brightness7Icon /> : <Brightness4Icon />;
  };
  const getDarkModeLabel = () => {
    if (darkMode === null) return 'Seguir sistema';
    return isDark ? 'Modo claro' : 'Modo oscuro';
  };

  // refs para cada mensaje animado
  const nodeRefs = useRef([]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ bgcolor: 'background.default' }}>
        <AppBar position="static" color="primary">
          <Toolbar>
            <SmartToyIcon sx={{ mr: 1 }} />
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              Chatbot de Asistencia Académica
            </Typography>
            <Tooltip title={getDarkModeLabel()}>
              <IconButton color="inherit" onClick={handleToggleDarkMode}>
                {getDarkModeIcon()}
              </IconButton>
            </Tooltip>
            <Badge color="success" variant="dot" sx={{ ml: 2 }}>
              <Typography variant="body2">En línea</Typography>
            </Badge>
          </Toolbar>
        </AppBar>
        <Container maxWidth="sm" sx={{ py: 5 }}>
          <Paper elevation={4} sx={{ p: 0, borderRadius: 3 }}>
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
            <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center', bgcolor: 'background.default', borderBottomLeftRadius: 12, borderBottomRightRadius: 12 }}>
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
    </ThemeProvider>
  );
}

export default App;
