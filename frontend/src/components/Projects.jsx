import React, { useState, useEffect } from 'react';
import Navigation from './Navigation';
import { projetsAPI } from '../services/api';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Chip,
  Box,
  IconButton,
  Alert
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  CheckCircle as CompleteIcon
} from '@mui/icons-material';

function Projects() {
  const [projects, setProjects] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [currentProject, setCurrentProject] = useState(null);
  const [formData, setFormData] = useState({
    titre: '',
    description: '',
    difficulte: 'medium',
    xp_recompense: 100,
    technos: ''
  });
  const [message, setMessage] = useState('');
  const user = JSON.parse(localStorage.getItem('user'));

  const difficultyLevels = [
    { value: 'facile', label: 'Facile', xp: 100, color: 'success' },
    { value: 'medium', label: 'Moyen', xp: 300, color: 'warning' },
    { value: 'difficile', label: 'Difficile', xp: 500, color: 'error' },
    { value: 'expert', label: 'Expert', xp: 800, color: 'error' }
  ];

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const response = await projetsAPI.getAll(user.id);
      setProjects(response.data);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  const handleOpenDialog = (project = null) => {
    if (project) {
      setCurrentProject(project);
      setFormData({
        titre: project.titre,
        description: project.description || '',
        difficulte: project.difficulte,
        xp_recompense: project.xp_recompense,
        technos: Array.isArray(project.technos) ? project.technos.join(', ') : ''
      });
    } else {
      setCurrentProject(null);
      setFormData({
        titre: '',
        description: '',
        difficulte: 'medium',
        xp_recompense: 300,
        technos: ''
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setCurrentProject(null);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    
    // Auto-set XP based on difficulty
    if (name === 'difficulte') {
      const level = difficultyLevels.find(l => l.value === value);
      if (level) {
        setFormData(prev => ({ ...prev, xp_recompense: level.xp }));
      }
    }
  };

  const handleSubmit = async () => {
    try {
      const projectData = {
        ...formData,
        technos: formData.technos.split(',').map(t => t.trim()).filter(t => t)
      };

      if (currentProject) {
        await projetsAPI.update(currentProject.id, projectData);
        setMessage('Projet mis à jour avec succès!');
      } else {
        await projetsAPI.create(projectData);
        setMessage('Projet créé avec succès!');
      }

      handleCloseDialog();
      loadProjects();
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      console.error('Error saving project:', error);
      setMessage('Erreur lors de la sauvegarde du projet');
    }
  };

  const handleComplete = async (project) => {
    try {
      await projetsAPI.update(project.id, { statut: 'termine' });
      setMessage(`🎉 +${project.xp_recompense} XP! Projet complété!`);
      loadProjects();
      
      // Update user XP in localStorage
      const updatedUser = { ...user, xp: user.xp + project.xp_recompense };
      localStorage.setItem('user', JSON.stringify(updatedUser));
      
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      console.error('Error completing project:', error);
    }
  };

  const handleDelete = async (projectId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce projet?')) {
      try {
        await projetsAPI.delete(projectId);
        setMessage('Projet supprimé');
        loadProjects();
        setTimeout(() => setMessage(''), 3000);
      } catch (error) {
        console.error('Error deleting project:', error);
      }
    }
  };

  const getDifficultyColor = (difficulte) => {
    const level = difficultyLevels.find(l => l.value === difficulte);
    return level ? level.color : 'default';
  };

  return (
    <>
      <Navigation />
    <Container sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">📁 Mes Projets</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Nouveau Projet
        </Button>
      </Box>

      {message && <Alert severity="success" sx={{ mb: 2 }}>{message}</Alert>}

      <Grid container spacing={3}>
        {projects.length === 0 ? (
          <Grid item xs={12}>
            <Typography color="text.secondary" align="center">
              Aucun projet. Créez votre premier projet!
            </Typography>
          </Grid>
        ) : (
          projects.map((project) => (
            <Grid item xs={12} md={6} lg={4} key={project.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="h6" component="div">
                      {project.titre}
                    </Typography>
                    <Chip
                      label={project.difficulte}
                      color={getDifficultyColor(project.difficulte)}
                      size="small"
                    />
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {project.description || 'Pas de description'}
                  </Typography>

                  {project.technos && project.technos.length > 0 && (
                    <Box sx={{ mb: 2 }}>
                      {project.technos.map((tech, idx) => (
                        <Chip
                          key={idx}
                          label={tech}
                          size="small"
                          sx={{ mr: 0.5, mb: 0.5 }}
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  )}

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="h6" color="primary">
                      {project.xp_recompense} XP
                    </Typography>
                    
                    <Box>
                      {project.statut !== 'termine' && (
                        <>
                          <IconButton
                            size="small"
                            color="success"
                            onClick={() => handleComplete(project)}
                            title="Marquer comme terminé"
                          >
                            <CompleteIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            color="primary"
                            onClick={() => handleOpenDialog(project)}
                          >
                            <EditIcon />
                          </IconButton>
                        </>
                      )}
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => handleDelete(project.id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  </Box>

                  {project.statut === 'termine' && (
                    <Chip
                      label="✓ Complété"
                      color="success"
                      size="small"
                      sx={{ mt: 1 }}
                    />
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))
        )}
      </Grid>

      {/* Add/Edit Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {currentProject ? 'Modifier le Projet' : 'Nouveau Projet'}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            name="titre"
            label="Titre du projet"
            fullWidth
            value={formData.titre}
            onChange={handleChange}
            required
          />
          <TextField
            margin="dense"
            name="description"
            label="Description"
            fullWidth
            multiline
            rows={3}
            value={formData.description}
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="difficulte"
            label="Difficulté"
            fullWidth
            select
            value={formData.difficulte}
            onChange={handleChange}
          >
            {difficultyLevels.map((level) => (
              <MenuItem key={level.value} value={level.value}>
                {level.label} - {level.xp} XP
              </MenuItem>
            ))}
          </TextField>
          <TextField
            margin="dense"
            name="xp_recompense"
            label="Récompense XP"
            fullWidth
            type="number"
            value={formData.xp_recompense}
            onChange={handleChange}
          />
          <TextField
            margin="dense"
            name="technos"
            label="Technologies (séparées par des virgules)"
            fullWidth
            value={formData.technos}
            onChange={handleChange}
            placeholder="React, Node.js, MongoDB"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Annuler</Button>
          <Button onClick={handleSubmit} variant="contained">
            {currentProject ? 'Mettre à jour' : 'Créer'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>    </>
  );
}
export default Projects;

