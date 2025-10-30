import React, { useState, useEffect } from 'react';
import Navigation from './Navigation';
import { useNavigate } from 'react-router-dom';
import { usersAPI, projetsAPI } from '../services/api';
import {
  Box,
  Container,
  Typography,
  Grid,
  Paper,
  Button,
  Avatar,
  Card,
  CardContent,
  LinearProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Folder as ProjectIcon,
} from '@mui/icons-material';

function Dashboard() {
  const [user, setUser] = useState(null);
  const [projects, setProjects] = useState([]);
  const [stats, setStats] = useState({ total: 0, completed: 0, inProgress: 0 });
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const userData = JSON.parse(localStorage.getItem('user'));
      setUser(userData);

      const response = await projetsAPI.getAll(userData.id);
      const userProjects = response.data;
      setProjects(userProjects);

      const completed = userProjects.filter(p => p.statut === 'termine').length;
      const inProgress = userProjects.filter(p => p.statut === 'en_cours').length;
      
      setStats({
        total: userProjects.length,
        completed,
        inProgress
      });
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const calculateLevel = (xp) => {
    return Math.floor(xp / 100) + 1;
  };

  const getXpProgress = (xp) => {
    return (
    <>
      <Navigation />xp % 100);
  };

  const menuItems = [
    { text: 'Tableau de Bord', icon: <HomeIcon />, path: '/dashboard' },
    { text: 'Mes Projets', icon: <ProjectIcon />, path: '/projects' },
    { text: 'Badges', icon: <BadgeIcon />, path: '/badges' },
    { text: 'Chat', icon: <ChatIcon />, path: '/chat' },
    { text: 'Calendrier', icon: <CalendarIcon />, path: '/calendar' },
    { text: 'Classement', icon: <LeaderboardIcon />, path: '/leaderboard' },
    { text: 'Profil', icon: <PersonIcon />, path: '/profile' }
  ];

  if (!user) return <Typography>Loading...</Typography>;

  return (
    <>
      <Navigation />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          {/* User Info Card */}
          <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
            <Grid container spacing={2} alignItems="center">
              <Grid item>
                <Avatar
                  sx={{ width: 80, height: 80, bgcolor: 'primary.main', fontSize: '2rem' }}
                >
                  {user.nom[0]}
                </Avatar>
              </Grid>
              <Grid item xs>
                <Typography variant="h4">{user.nom}</Typography>
                <Typography variant="subtitle1" color="text.secondary">
                  {user.promo} • {user.role}
                </Typography>
                <Box sx={{ mt: 1 }}>
                  <Typography variant="body2">
                    Niveau {calculateLevel(user.xp)} • {user.xp} XP
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={getXpProgress(user.xp)}
                    sx={{ mt: 1, height: 8, borderRadius: 4 }}
                  />
                </Box>
              </Grid>
            </Grid>
          </Paper>

          {/* Quick Access Buttons */}
          <Grid container spacing={2} sx={{ mb: 4 }}>
            <Grid item xs={6} sm={4} md={2}>
              <Button
                fullWidth
                variant="contained"
                startIcon={<ProjectIcon />}
                onClick={() => navigate('/projects')}
              >
                Projets
              </Button>
            </Grid>
            <Grid item xs={6} sm={4} md={2}>
              <Button
                fullWidth
                variant="contained"
                startIcon={<BadgeIcon />}
                onClick={() => navigate('/badges')}
              >
                Badges
              </Button>
            </Grid>
            <Grid item xs={6} sm={4} md={2}>
              <Button
                fullWidth
                variant="contained"
                startIcon={<ChatIcon />}
                onClick={() => navigate('/chat')}
              >
                Chat
              </Button>
            </Grid>
            <Grid item xs={6} sm={4} md={2}>
              <Button
                fullWidth
                variant="contained"
                startIcon={<CalendarIcon />}
                onClick={() => navigate('/calendar')}
              >
                Événements
              </Button>
            </Grid>
            <Grid item xs={6} sm={4} md={2}>
              <Button
                fullWidth
                variant="contained"
                startIcon={<LeaderboardIcon />}
                onClick={() => navigate('/leaderboard')}
              >
                Classement
              </Button>
            </Grid>
            <Grid item xs={6} sm={4} md={2}>
              <Button
                fullWidth
                variant="contained"
                startIcon={<PersonIcon />}
                onClick={() => navigate('/profile')}
              >
                Profil
              </Button>
            </Grid>
          </Grid>

          {/* Stats Cards */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Projets Total
                  </Typography>
                  <Typography variant="h4">{stats.total}</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    Complétés
                  </Typography>
                  <Typography variant="h4" color="success.main">
                    {stats.completed}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    En cours
                  </Typography>
                  <Typography variant="h4" color="warning.main">
                    {stats.inProgress}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Projects Section */}
          <Paper elevation={3} sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
              <Typography variant="h5">Mes Projets</Typography>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => navigate('/projects')}
              >
                Nouveau Projet
              </Button>
            </Box>

            {projects.length === 0 ? (
              <Typography color="text.secondary">
                Aucun projet pour le moment. Créez votre premier projet!
              </Typography>
            ) : (
              <Grid container spacing={2}>
                {projects.slice(0, 6).map((project) => (
                  <Grid item xs={12} md={6} key={project.id}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6" gutterBottom>
                          {project.titre}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {project.description || 'Pas de description'}
                        </Typography>
                        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between' }}>
                          <Typography variant="caption">
                            Statut: {project.statut}
                          </Typography>
                          <Typography variant="caption" color="primary">
                            {project.xp_recompense} XP
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            )}

            {projects.length > 6 && (
              <Button
                fullWidth
                sx={{ mt: 2 }}
                onClick={() => navigate('/projects')}
              >
                Voir tous les projets
              </Button>
            )}
          </Paper>
        </Container>
    </>
  );
}
export default Dashboard;

