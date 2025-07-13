import React, { useEffect } from 'react';
import { Box, CssBaseline } from '@mui/material';
import { ThemeProvider } from '@mui/material/styles';
import { Header } from './components/common/Header';
import { ChatContainer } from './components/Chat/ChatContainer';
import { useTheme } from './hooks/useTheme';
import { useChat } from './hooks/useChat';
import './App.css';
import './styles/darkMode.css';

function App() {
  const { isDark, theme, toggleDarkMode, getDarkModeIcon, getDarkModeLabel } = useTheme();
  const { messages, isLoading, chatEndRef, sendMessage, askQuestion, clearChat, handleCategoryClick } = useChat();

  useEffect(() => {
    // Cambia el atributo data-theme del body para modo oscuro elegante
    document.body.setAttribute('data-theme', isDark ? 'dark' : 'light');
  }, [isDark]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ bgcolor: 'background.default' }}>
        <Header 
          onToggleDarkMode={toggleDarkMode}
          darkModeIcon={getDarkModeIcon()}
          darkModeLabel={getDarkModeLabel()}
        />
        <ChatContainer 
          messages={messages}
          chatEndRef={chatEndRef}
          onSendMessage={sendMessage}
          onAskQuestion={askQuestion}
          onClearChat={clearChat}
          isLoading={isLoading}
          onCategoryClick={handleCategoryClick}
        />
      </Box>
    </ThemeProvider>
  );
}

export default App;
