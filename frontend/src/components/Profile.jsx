import React, { useState, useEffect } from 'react';
import Navigation from './Navigation';
import { usersAPI } from '../services/api';
import {
  Container,
  Paper,
  Box,
  Typography,
  Avatar,
  Button,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import {
  Edit as EditIcon,
  Lock as LockIcon,
  EmojiEvents as BadgeIcon
} from '@mui/icons-material';

function Profile() {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));
  const [openEdit, setOpenEdit] = useState(false);
  const [openPassword, setOpenPassword] = useState(false);
  const [editData, setEditData] = useState({
    nom: '',
    email: '',
    promo: '',
    bio: ''
  });
  const [passwordData, setPasswordData] = useState({
    old_password: '',
    new_password: '',
    confirm_password: ''
  });

  useEffect(() => {
    loadUserProfile();
  }, []);

  const loadUserProfile = async () => {
    try {
      const response = await usersAPI.getById(user.id);
      setUser(response.data);
      localStorage.setItem('user', JSON.stringify(response.data));
    } catch (error) {
      console.error('Error loading profile:', error);
    }
  };

  const calculateLevel = (xp) => {
    return Math.floor(xp / 100) + 1;
  };

  const getXpProgress = (xp) => {
    return (
    <>
      <Navigation />xp % 100);
  };

  const getXpForNextLevel = (xp) => {
    const currentLevel = calculateLevel(xp);
    return currentLevel * 100;
  };

  const handleEditOpen = () => {
    setEditData({
      nom: user.nom,
      email: user.email,
      promo: user.promo,
      bio: user.bio || ''
    });
    setOpenEdit(true);
  };

  const handleEditSave = async () => {
    try {
      await usersAPI.update(user.id, editData);
      await loadUserProfile();
      setOpenEdit(false);
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  };

  const handlePasswordSave = async () => {
    if (passwordData.new_password !== passwordData.confirm_password) {
      alert('Les mots de passe ne correspondent pas');
      return;
    }

    try {
      await usersAPI.changePassword(user.id, {
        old_password: passwordData.old_password,
        new_password: passwordData.new_password
      });
      setOpenPassword(false);
      setPasswordData({ old_password: '', new_password: '', confirm_password: '' });
      alert('Mot de passe changé avec succès!');
    } catch (error) {
      alert('Erreur: Vérifiez votre ancien mot de passe');
    }
  };

  return (
    <>
      <Navigation />
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Grid container spacing={3}>
        {/* Profile Header */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Grid container spacing={3} alignItems="center">
              <Grid item>
                <Avatar
                  src={user.avatar}
                  sx={{ width: 120, height: 120, fontSize: '3rem', bgcolor: 'primary.main' }}
                >
                  {user.nom[0]}
                </Avatar>
              </Grid>
              <Grid item xs>
                <Typography variant="h4">{user.nom}</Typography>
                <Typography variant="body1" color="text.secondary" gutterBottom>
                  {user.email} • {user.promo}
                </Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  {user.bio || 'Aucune biographie'}
                </Typography>
                <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                  <Button
                    variant="outlined"
                    startIcon={<EditIcon />}
                    onClick={handleEditOpen}
                  >
                    Modifier le profil
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<LockIcon />}
                    onClick={() => setOpenPassword(true)}
                  >
                    Changer le mot de passe
                  </Button>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* XP & Level */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📊 Niveau & XP
              </Typography>
              <Typography variant="h3" color="primary" align="center">
                Niveau {calculateLevel(user.xp)}
              </Typography>
              <Typography variant="body2" color="text.secondary" align="center" gutterBottom>
                {user.xp} / {getXpForNextLevel(user.xp)} XP
              </Typography>
              <LinearProgress
                variant="determinate"
                value={getXpProgress(user.xp)}
                sx={{ height: 10, borderRadius: 5 }}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Stats */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📈 Statistiques
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Projets complétés
                </Typography>
                <Typography variant="h4" color="success.main">
                  {user.projets_count || 0}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Badges */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🏆 Badges
              </Typography>
              <Typography variant="h4" color="warning.main">
                {user.badges_count || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                badges débloqués
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Role Badge */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              🎭 Rôle
            </Typography>
            <Chip
              label={user.role === 'admin' ? '👑 Administrateur' : '👤 Étudiant'}
              color={user.role === 'admin' ? 'error' : 'primary'}
              size="large"
            />
          </Paper>
        </Grid>
      </Grid>

      {/* Edit Profile Dialog */}
      <Dialog open={openEdit} onClose={() => setOpenEdit(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Modifier le profil</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            margin="normal"
            label="Nom"
            value={editData.nom}
            onChange={(e) => setEditData({ ...editData, nom: e.target.value })}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Email"
            value={editData.email}
            onChange={(e) => setEditData({ ...editData, email: e.target.value })}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Promo"
            value={editData.promo}
            onChange={(e) => setEditData({ ...editData, promo: e.target.value })}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Bio"
            multiline
            rows={3}
            value={editData.bio}
            onChange={(e) => setEditData({ ...editData, bio: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEdit(false)}>Annuler</Button>
          <Button onClick={handleEditSave} variant="contained">Enregistrer</Button>
        </DialogActions>
      </Dialog>

      {/* Change Password Dialog */}
      <Dialog open={openPassword} onClose={() => setOpenPassword(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Changer le mot de passe</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            margin="normal"
            label="Ancien mot de passe"
            type="password"
            value={passwordData.old_password}
            onChange={(e) => setPasswordData({ ...passwordData, old_password: e.target.value })}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Nouveau mot de passe"
            type="password"
            value={passwordData.new_password}
            onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Confirmer le mot de passe"
            type="password"
            value={passwordData.confirm_password}
            onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenPassword(false)}>Annuler</Button>
          <Button onClick={handlePasswordSave} variant="contained">Changer</Button>
        </DialogActions>
      </Dialog>
    </Container>    </>
  );
}
export default Profile;

