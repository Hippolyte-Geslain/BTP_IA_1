import React, { useState, useEffect, useRef } from 'react';
import Navigation from './Navigation';
import { chatAPI } from '../services/api';
import {
  Container,
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  List,
  ListItem,
  Avatar,
  Divider
} from '@mui/material';
import { Send as SendIcon } from '@mui/icons-material';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const user = JSON.parse(localStorage.getItem('user'));

  useEffect(() => {
    loadMessages();
    const interval = setInterval(loadMessages, 5000); // Refresh every 5 seconds
    return (
    <>
      <Navigation />) => clearInterval(interval);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadMessages = async () => {
    try {
      const response = await chatAPI.getMessages();
      setMessages(response.data);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    setLoading(true);
    try {
      await chatAPI.sendMessage({ contenu: newMessage });
      setNewMessage('');
      await loadMessages();
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <>
      <Navigation />
    <Container maxWidth="md" sx={{ height: '100vh', display: 'flex', flexDirection: 'column', py: 2 }}>
      <Typography variant="h4" gutterBottom>
        💬 Chat en Direct
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        Discutez avec les autres étudiants
      </Typography>

      <Paper
        sx={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          mt: 2
        }}
      >
        {/* Messages List */}
        <Box
          sx={{
            flex: 1,
            overflow: 'auto',
            p: 2,
            bgcolor: 'background.default'
          }}
        >
          <List>
            {messages.length === 0 ? (
              <Typography color="text.secondary" align="center">
                Aucun message. Soyez le premier à discuter!
              </Typography>
            ) : (
              messages.map((msg, index) => (
                <React.Fragment key={msg.id || index}>
                  <ListItem
                    sx={{
                      display: 'flex',
                      flexDirection: msg.user_id === user.id ? 'row-reverse' : 'row',
                      alignItems: 'flex-start'
                    }}
                  >
                    <Avatar
                      sx={{
                        bgcolor: msg.user_id === user.id ? 'primary.main' : 'secondary.main',
                        mx: 1
                      }}
                    >
                      {msg.user?.nom?.[0] || '?'}
                    </Avatar>
                    <Box
                      sx={{
                        maxWidth: '70%',
                        bgcolor: msg.user_id === user.id ? 'primary.light' : 'grey.200',
                        borderRadius: 2,
                        p: 1.5
                      }}
                    >
                      <Typography variant="caption" color="text.secondary">
                        {msg.user?.nom || 'Anonyme'} • {formatTime(msg.timestamp)}
                      </Typography>
                      <Typography variant="body1" sx={{ mt: 0.5, wordBreak: 'break-word' }}>
                        {msg.contenu}
                      </Typography>
                    </Box>
                  </ListItem>
                  {index < messages.length - 1 && <Divider variant="inset" component="li" />}
                </React.Fragment>
              ))
            )}
            <div ref={messagesEndRef} />
          </List>
        </Box>

        {/* Message Input */}
        <Box
          component="form"
          onSubmit={handleSend}
          sx={{
            p: 2,
            bgcolor: 'background.paper',
            borderTop: 1,
            borderColor: 'divider'
          }}
        >
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              fullWidth
              placeholder="Écrivez votre message..."
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              disabled={loading}
              autoComplete="off"
            />
            <Button
              type="submit"
              variant="contained"
              endIcon={<SendIcon />}
              disabled={loading || !newMessage.trim()}
            >
              Envoyer
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>    </>
  );
}
export default Chat;

