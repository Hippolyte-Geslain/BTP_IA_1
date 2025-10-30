import React, { useState, useEffect } from 'react';
import Navigation from './Navigation';
import { usersAPI } from '../services/api';
import {
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Avatar,
  Chip,
  Box
} from '@mui/material';
import {
  EmojiEvents as TrophyIcon
} from '@mui/icons-material';

function Leaderboard() {
  const [users, setUsers] = useState([]);
  const currentUser = JSON.parse(localStorage.getItem('user'));

  useEffect(() => {
    loadLeaderboard();
  }, []);

  const loadLeaderboard = async () => {
    try {
      const response = await usersAPI.getLeaderboard();
      setUsers(response.data);
    } catch (error) {
      console.error('Error loading leaderboard:', error);
    }
  };

  const getMedalIcon = (rank) => {
    switch (rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return `#${rank}`;
    }
  };

  const getMedalColor = (rank) => {
    switch (rank) {
      case 1: return 'gold';
      case 2: return 'silver';
      case 3: return '#CD7F32';
      default: return 'text.secondary';
    }
  };

  return (
    <>
      <Navigation />
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <TrophyIcon sx={{ fontSize: 40, mr: 2, color: 'warning.main' }} />
        <Typography variant="h4">
          🏆 Classement des Étudiants
        </Typography>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow sx={{ bgcolor: 'primary.main' }}>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Rang</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Étudiant</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Promo</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }} align="right">XP</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }} align="right">Niveau</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow
                key={user.id}
                sx={{
                  bgcolor: user.id === currentUser.id ? 'action.selected' : 'inherit',
                  '&:hover': { bgcolor: 'action.hover' }
                }}
              >
                <TableCell>
                  <Typography
                    variant="h6"
                    sx={{
                      color: getMedalColor(user.rank),
                      fontWeight: 'bold'
                    }}
                  >
                    {getMedalIcon(user.rank)}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Avatar src={user.avatar} sx={{ bgcolor: 'primary.main' }}>
                      {user.nom[0]}
                    </Avatar>
                    <Box>
                      <Typography variant="body1" fontWeight="medium">
                        {user.nom}
                        {user.id === currentUser.id && (
                          <Chip label="Vous" size="small" sx={{ ml: 1 }} color="primary" />
                        )}
                      </Typography>
                    </Box>
                  </Box>
                </TableCell>
                <TableCell>
                  <Chip label={user.promo} size="small" />
                </TableCell>
                <TableCell align="right">
                  <Typography variant="body1" fontWeight="bold" color="primary">
                    {user.xp} XP
                  </Typography>
                </TableCell>
                <TableCell align="right">
                  <Chip label={`Niveau ${user.niveau}`} color="success" />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {users.length === 0 && (
        <Typography align="center" color="text.secondary" sx={{ mt: 4 }}>
          Aucun étudiant dans le classement
        </Typography>
      )}
    </Container>    </>
  );
}
export default Leaderboard;

