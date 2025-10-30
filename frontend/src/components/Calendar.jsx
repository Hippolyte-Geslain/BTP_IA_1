import React, { useState } from 'react';
import Navigation from './Navigation';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  Button
} from '@mui/material';
import {
  Event as EventIcon,
  LocationOn as LocationIcon,
  Person as PersonIcon
} from '@mui/icons-material';

function Calendar() {
  // Mock events - in real app, fetch from API
  const [events] = useState([
    {
      id: 1,
      titre: '🎉 Soirée BDE',
      date: '2024-12-15',
      type: 'BDE',
      lieu: 'Campus La Plateforme',
      participants: 45,
      description: 'Grande soirée de fin d\'année organisée par le BDE'
    },
    {
      id: 2,
      titre: '💻 Workshop React',
      date: '2024-12-20',
      type: 'Workshop',
      lieu: 'Salle 301',
      participants: 20,
      description: 'Atelier pratique sur React et les hooks'
    },
    {
      id: 3,
      titre: '🏆 Tournoi Code',
      date: '2025-01-10',
      type: 'Tournoi',
      lieu: 'En ligne',
      participants: 30,
      description: 'Compétition de programmation avec récompenses'
    },
    {
      id: 4,
      titre: '📚 Formation Git',
      date: '2024-12-18',
      type: 'Workshop',
      lieu: 'Salle 201',
      participants: 15,
      description: 'Maîtriser Git et GitHub'
    },
    {
      id: 5,
      titre: '🎮 Game Jam',
      date: '2025-01-15',
      type: 'Hackathon',
      lieu: 'Campus',
      participants: 25,
      description: 'Créez un jeu en 48h'
    }
  ]);

  const getEventColor = (type) => {
    switch (type) {
      case 'BDE': return 'error';
      case 'Workshop': return 'primary';
      case 'Tournoi': return 'warning';
      case 'Hackathon': return 'success';
      default: return 'default';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const isUpcoming = (dateString) => {
    return new Date(dateString) > new Date();
  };

  const handleParticipate = (event) => {
    alert(`Vous participez à: ${event.titre}`);
  };

  return (
    <>
      <Navigation />
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        📅 Calendrier des Événements
      </Typography>
      <Typography variant="body1" color="text.secondary" gutterBottom>
        Découvrez tous les événements de La Plateforme_
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {events.map((event) => (
          <Grid item xs={12} md={6} key={event.id}>
            <Card
              sx={{
                height: '100%',
                opacity: isUpcoming(event.date) ? 1 : 0.7
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                  <Typography variant="h6" component="div">
                    {event.titre}
                  </Typography>
                  <Chip
                    label={event.type}
                    color={getEventColor(event.type)}
                    size="small"
                  />
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                  <EventIcon fontSize="small" color="action" />
                  <Typography variant="body2" color="text.secondary">
                    {formatDate(event.date)}
                  </Typography>
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                  <LocationIcon fontSize="small" color="action" />
                  <Typography variant="body2" color="text.secondary">
                    {event.lieu}
                  </Typography>
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                  <PersonIcon fontSize="small" color="action" />
                  <Typography variant="body2" color="text.secondary">
                    {event.participants} participants
                  </Typography>
                </Box>

                <Typography variant="body2" sx={{ mb: 2 }}>
                  {event.description}
                </Typography>

                {isUpcoming(event.date) && (
                  <Button
                    variant="contained"
                    fullWidth
                    onClick={() => handleParticipate(event)}
                  >
                    Participer
                  </Button>
                )}

                {!isUpcoming(event.date) && (
                  <Chip label="Événement passé" size="small" />
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>    </>
  );
}
export default Calendar;

