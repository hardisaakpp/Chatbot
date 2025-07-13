import React from 'react';
import {
  Container,
  Paper,
  Divider
} from '@mui/material';
import { MessageList } from './MessageList';
import { QuickActions } from './QuickActions';
import { MessageInput } from './MessageInput';
import { ChatFooter } from './ChatFooter';

export const ChatContainer = ({ 
  messages, 
  chatEndRef, 
  onSendMessage, 
  onAskQuestion, 
  onClearChat, 
  isLoading,
  onCategoryClick
}) => {
  return (
    <Container maxWidth="sm" sx={{ py: 5 }}>
      <Paper elevation={4} sx={{ p: 0, borderRadius: 3 }}>
        <MessageList messages={messages} chatEndRef={chatEndRef} onCategoryClick={onCategoryClick} />
        <Divider />
        <QuickActions onAskQuestion={onAskQuestion} isLoading={isLoading} />
        <Divider />
        <MessageInput onSendMessage={onSendMessage} isLoading={isLoading} />
        <Divider />
        <ChatFooter 
          onClearChat={onClearChat} 
          messageCount={messages.length} 
          isLoading={isLoading} 
        />
      </Paper>
    </Container>
  );
}; 