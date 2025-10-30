import React, { useState } from 'react';
import Navigation from './Navigation';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Chip
} from '@mui/material';
import {
  Lock as LockIcon,
  CheckCircle as UnlockedIcon
} from '@mui/icons-material';

function Badges() {
  const user = JSON.parse(localStorage.getItem('user'));

  // All available badges
  const allBadges = [
    {
      id: 1,
      nom: '🏆 Premier Projet',
      description: 'Complétez votre premier projet',
      icone: '🏆',
      condition: 'projets_completes >= 1',
      unlocked: (user.projets_count || 0) >= 1
    },
    {
      id: 2,
      nom: '🎓 Mentor',
      description: 'Aidez 5 autres étudiants',
      icone: '🎓',
      condition: 'aides_donnees >= 5',
      unlocked: false
    },
    {
      id: 3,
      nom: '💯 Centurion',
      description: 'Atteignez 100 XP',
      icone: '💯',
      condition: 'xp >= 100',
      unlocked: user.xp >= 100
    },
    {
      id: 4,
      nom: '🔥 En Feu!',
      description: 'Complétez 5 projets',
      icone: '🔥',
      condition: 'projets_completes >= 5',
      unlocked: (user.projets_count || 0) >= 5
    },
    {
      id: 5,
      nom: '🌟 Étoile Montante',
      description: 'Atteignez le niveau 5',
      icone: '🌟',
      condition: 'niveau >= 5',
      unlocked: user.niveau >= 5
    },
    {
      id: 6,
      nom: '💬 Bavard',
      description: 'Envoyez 50 messages dans le chat',
      icone: '💬',
      condition: 'messages >= 50',
      unlocked: false
    },
    {
      id: 7,
      nom: '🎯 Perfectionniste',
      description: 'Complétez tous les projets difficiles',
      icone: '🎯',
      condition: 'projets_difficiles_completes >= 3',
      unlocked: false
    },
    {
      id: 8,
      nom: '👑 Légende',
      description: 'Atteignez 1000 XP',
      icone: '👑',
      condition: 'xp >= 1000',
      unlocked: user.xp >= 1000
    },
    {
      id: 9,
      nom: '🤝 Collaborateur',
      description: 'Participez à 3 projets de groupe',
      icone: '🤝',
      condition: 'projets_groupe >= 3',
      unlocked: false
    },
    {
      id: 10,
      nom: '⚡ Rapide',
      description: 'Complétez un projet en moins de 24h',
      icone: '⚡',
      condition: 'projet_rapide',
      unlocked: false
    },
    {
      id: 11,
      nom: '🎨 Créatif',
      description: 'Créez 10 projets uniques',
      icone: '🎨',
      condition: 'projets_crees >= 10',
      unlocked: false
    },
    {
      id: 12,
      nom: '🏅 Champion',
      description: 'Gagnez un tournoi',
      icone: '🏅',
      condition: 'tournois_gagnes >= 1',
      unlocked: false
    }
  ];

  const unlockedBadges = allBadges.filter(b => b.unlocked);
  const lockedBadges = allBadges.filter(b => !b.unlocked);

  return (
    <>
      <Navigation />
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        🏆 Mes Badges
      </Typography>
      <Typography variant="body1" color="text.secondary" gutterBottom>
        {unlockedBadges.length} / {allBadges.length} badges débloqués
      </Typography>

      {/* Unlocked Badges */}
      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <UnlockedIcon color="success" />
          Badges Débloqués ({unlockedBadges.length})
        </Typography>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          {unlockedBadges.length === 0 ? (
            <Grid item xs={12}>
              <Typography color="text.secondary">
                Aucun badge débloqué pour le moment. Complétez des projets pour en obtenir!
              </Typography>
            </Grid>
          ) : (
            unlockedBadges.map((badge) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={badge.id}>
                <Card
                  sx={{
                    height: '100%',
                    bgcolor: 'success.light',
                    border: 2,
                    borderColor: 'success.main'
                  }}
                >
                  <CardContent sx={{ textAlign: 'center' }}>
                    <Typography variant="h2" sx={{ mb: 1 }}>
                      {badge.icone}
                    </Typography>
                    <Typography variant="h6" gutterBottom>
                      {badge.nom}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {badge.description}
                    </Typography>
                    <Chip
                      label="Débloqué ✓"
                      color="success"
                      size="small"
                      sx={{ mt: 2 }}
                    />
                  </CardContent>
                </Card>
              </Grid>
            ))
          )}
        </Grid>
      </Box>

      {/* Locked Badges */}
      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <LockIcon />
          Badges Verrouillés ({lockedBadges.length})
        </Typography>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          {lockedBadges.map((badge) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={badge.id}>
              <Card
                sx={{
                  height: '100%',
                  bgcolor: 'action.disabledBackground',
                  opacity: 0.6
                }}
              >
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h2" sx={{ mb: 1, filter: 'grayscale(100%)' }}>
                    {badge.icone}
                  </Typography>
                  <Typography variant="h6" gutterBottom>
                    {badge.nom}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {badge.description}
                  </Typography>
                  <Chip
                    icon={<LockIcon />}
                    label="Verrouillé"
                    size="small"
                    sx={{ mt: 2 }}
                  />
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>    </>
  );
}
export default Badges;

