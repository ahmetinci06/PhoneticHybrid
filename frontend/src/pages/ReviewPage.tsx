import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Alert,
  Divider,
  Stack,
} from '@mui/material';
import {
  PlayArrow,
  Pause,
  CheckCircle,
  RadioButtonUnchecked,
  PersonOutline,
  AssignmentTurnedIn,
  MusicNote,
} from '@mui/icons-material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

interface ParticipantSummary {
  participant_id: string;
  total_recordings: number;
  labeled_recordings: number;
  unlabeled_recordings: number;
  registration_date: string | null;
  survey_completed: boolean;
}

interface RecordingInfo {
  filename: string;
  word: string;
  audio_path: string;
  labeled: boolean;
  score: number | null;
  evaluator: string | null;
  notes: string | null;
  timestamp: string | null;
}

interface ParticipantDetails {
  participant_id: string;
  info: any;
  survey: any;
  recordings: RecordingInfo[];
  stats: {
    total_recordings: number;
    labeled: number;
    unlabeled: number;
  };
}

interface LabelingStats {
  total_participants: number;
  total_recordings: number;
  labeled_recordings: number;
  unlabeled_recordings: number;
  labeling_progress: number;
}

const ReviewPage: React.FC = () => {
  const [participants, setParticipants] = useState<ParticipantSummary[]>([]);
  const [selectedParticipant, setSelectedParticipant] = useState<ParticipantDetails | null>(null);
  const [stats, setStats] = useState<LabelingStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [labelDialogOpen, setLabelDialogOpen] = useState(false);
  const [currentRecording, setCurrentRecording] = useState<RecordingInfo | null>(null);
  const [audioPlaying, setAudioPlaying] = useState<string | null>(null);
  const [audioElement, setAudioElement] = useState<HTMLAudioElement | null>(null);

  // Label form state
  const [score, setScore] = useState<number>(75);
  const [notes, setNotes] = useState<string>('');
  const [quality, setQuality] = useState<string>('good');
  const [evaluator, setEvaluator] = useState<string>('');
  const [specificIssues, setSpecificIssues] = useState<string[]>([]);

  useEffect(() => {
    loadParticipants();
    loadStats();
  }, []);

  const loadParticipants = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/review/participants`);
      setParticipants(response.data);
    } catch (error) {
      console.error('Failed to load participants:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/review/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const loadParticipantDetails = async (participantId: string) => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/review/participants/${participantId}`);
      setSelectedParticipant(response.data);
    } catch (error) {
      console.error('Failed to load participant details:', error);
    } finally {
      setLoading(false);
    }
  };

  const playAudio = (audioPath: string) => {
    if (audioElement) {
      audioElement.pause();
    }

    if (audioPlaying === audioPath) {
      setAudioPlaying(null);
      setAudioElement(null);
      return;
    }

    const audio = new Audio(`${API_BASE_URL}${audioPath}`);
    audio.play();
    setAudioPlaying(audioPath);
    setAudioElement(audio);

    audio.onended = () => {
      setAudioPlaying(null);
      setAudioElement(null);
    };
  };

  const openLabelDialog = (recording: RecordingInfo) => {
    setCurrentRecording(recording);
    
    // Load existing label if available
    if (recording.labeled && recording.score !== null) {
      setScore(recording.score);
      setNotes(recording.notes || '');
      setEvaluator(recording.evaluator || '');
    } else {
      setScore(75);
      setNotes('');
      setEvaluator('');
    }
    
    setLabelDialogOpen(true);
  };

  const saveLabel = async () => {
    if (!currentRecording || !selectedParticipant) return;

    try {
      await axios.post(
        `${API_BASE_URL}/review/label/${selectedParticipant.participant_id}/${currentRecording.filename}`,
        {
          word: currentRecording.word,
          score: score,
          evaluator: evaluator,
          notes: notes,
          pronunciation_quality: quality,
          specific_issues: specificIssues,
          timestamp: new Date().toISOString(),
        }
      );

      // Reload participant details
      await loadParticipantDetails(selectedParticipant.participant_id);
      await loadParticipants();
      await loadStats();
      
      setLabelDialogOpen(false);
      setCurrentRecording(null);
    } catch (error) {
      console.error('Failed to save label:', error);
      alert('Failed to save label');
    }
  };

  const getQualityColor = (quality: string) => {
    switch (quality) {
      case 'excellent': return 'success';
      case 'good': return 'primary';
      case 'fair': return 'warning';
      case 'poor': return 'error';
      default: return 'default';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'success';
    if (score >= 80) return 'primary';
    if (score >= 70) return 'warning';
    return 'error';
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Typography variant="h3" gutterBottom>
        📋 Pronunciation Review & Data Management
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Review participant recordings, listen to pronunciations, and optionally add manual quality assessments.
        Recordings are automatically analyzed using Whisper speech recognition.
      </Typography>
      <Alert severity="info" sx={{ mb: 3 }}>
        <strong>Automatic Analysis Active:</strong> All recordings are automatically analyzed using Whisper (OpenAI) + Phoneme Analysis.
        Manual labeling is optional and can be used for quality assurance or research purposes.
      </Alert>

      {/* Overall Stats */}
      {stats && (
        <Card sx={{ mb: 4, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
          <CardContent>
            <Grid container spacing={3}>
              <Grid item xs={12} md={3}>
                <Typography variant="h4">{stats.total_participants}</Typography>
                <Typography variant="body2">Total Participants</Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="h4">{stats.total_recordings}</Typography>
                <Typography variant="body2">Total Recordings</Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="h4">{stats.labeled_recordings}</Typography>
                <Typography variant="body2">Manually Reviewed</Typography>
              </Grid>
              <Grid item xs={12} md={3}>
                <Typography variant="h4">{stats.unlabeled_recordings}</Typography>
                <Typography variant="body2">Awaiting Manual Review</Typography>
              </Grid>
              <Grid item xs={12}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Typography variant="body2">Manual Review Progress:</Typography>
                  <Box sx={{ flexGrow: 1 }}>
                    <LinearProgress 
                      variant="determinate" 
                      value={stats.labeling_progress} 
                      sx={{ height: 10, borderRadius: 5, bgcolor: 'rgba(255,255,255,0.3)' }}
                    />
                  </Box>
                  <Typography variant="body2">{stats.labeling_progress.toFixed(1)}%</Typography>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      <Grid container spacing={3}>
        {/* Participants List */}
        <Grid item xs={12} md={selectedParticipant ? 4 : 12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                <PersonOutline sx={{ verticalAlign: 'middle', mr: 1 }} />
                Participants
              </Typography>
              <Divider sx={{ my: 2 }} />
              
              {loading && <LinearProgress />}
              
              <TableContainer sx={{ maxHeight: 600 }}>
                <Table size="small" stickyHeader>
                  <TableHead>
                    <TableRow>
                      <TableCell>ID</TableCell>
                      <TableCell align="center">Recordings</TableCell>
                      <TableCell align="center">Labeled</TableCell>
                      <TableCell align="center">Survey</TableCell>
                      <TableCell align="center">Action</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {participants.map((participant) => (
                      <TableRow 
                        key={participant.participant_id}
                        selected={selectedParticipant?.participant_id === participant.participant_id}
                      >
                        <TableCell>
                          <Typography variant="body2" noWrap sx={{ maxWidth: 150 }}>
                            {participant.participant_id.replace('participant_', '')}
                          </Typography>
                        </TableCell>
                        <TableCell align="center">
                          <Chip 
                            label={participant.total_recordings} 
                            size="small" 
                            color="primary" 
                            variant="outlined"
                          />
                        </TableCell>
                        <TableCell align="center">
                          <Chip 
                            label={`${participant.labeled_recordings}/${participant.total_recordings}`}
                            size="small"
                            color={participant.labeled_recordings === participant.total_recordings ? 'success' : 'warning'}
                          />
                        </TableCell>
                        <TableCell align="center">
                          {participant.survey_completed ? (
                            <CheckCircle color="success" fontSize="small" />
                          ) : (
                            <RadioButtonUnchecked color="disabled" fontSize="small" />
                          )}
                        </TableCell>
                        <TableCell align="center">
                          <Button
                            size="small"
                            onClick={() => loadParticipantDetails(participant.participant_id)}
                            variant={selectedParticipant?.participant_id === participant.participant_id ? 'contained' : 'outlined'}
                          >
                            View
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Participant Details */}
        {selectedParticipant && (
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h5">
                    Participant Details
                  </Typography>
                  <Button onClick={() => setSelectedParticipant(null)} variant="outlined" size="small">
                    Close
                  </Button>
                </Box>
                
                <Divider sx={{ my: 2 }} />

                {/* Participant Info */}
                {selectedParticipant.info && (
                  <Box sx={{ mb: 3, p: 2, bgcolor: 'background.default', borderRadius: 1 }}>
                    <Typography variant="h6" gutterBottom>
                      <PersonOutline sx={{ verticalAlign: 'middle', mr: 1 }} />
                      Participant Information
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Name:</Typography>
                        <Typography variant="body1">{selectedParticipant.info.name || 'N/A'}</Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Age:</Typography>
                        <Typography variant="body1">{selectedParticipant.info.age || 'N/A'}</Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Gender:</Typography>
                        <Typography variant="body1">{selectedParticipant.info.gender || 'N/A'}</Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Consent Given:</Typography>
                        <Typography variant="body1">{selectedParticipant.info.consent ? 'Yes' : 'No'}</Typography>
                      </Grid>
                    </Grid>
                  </Box>
                )}

                {/* Survey Responses */}
                {selectedParticipant.survey && selectedParticipant.survey.responses && (
                  <Box sx={{ mb: 3, p: 2, bgcolor: 'background.default', borderRadius: 1 }}>
                    <Typography variant="h6" gutterBottom>
                      <AssignmentTurnedIn sx={{ verticalAlign: 'middle', mr: 1 }} />
                      Orthodontic Knowledge Survey
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {selectedParticipant.survey.responses.length} questions answered
                    </Typography>
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
                      Average score: {(selectedParticipant.survey.responses.reduce((a: number, b: number) => a + b, 0) / selectedParticipant.survey.responses.length).toFixed(1)}/5
                    </Typography>
                  </Box>
                )}

                {/* Recordings */}
                <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                  <MusicNote sx={{ verticalAlign: 'middle', mr: 1 }} />
                  Recordings ({selectedParticipant.stats.labeled}/{selectedParticipant.stats.total_recordings} labeled)
                </Typography>

                <TableContainer component={Paper} variant="outlined">
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Word</TableCell>
                        <TableCell align="center">Audio</TableCell>
                        <TableCell align="center">Status</TableCell>
                        <TableCell align="center">Score</TableCell>
                        <TableCell align="center">Evaluator</TableCell>
                        <TableCell align="center">Action</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {selectedParticipant.recordings.map((recording) => (
                        <TableRow key={recording.filename}>
                          <TableCell>
                            <Typography variant="body2" fontWeight="bold">
                              {recording.word}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {recording.filename}
                            </Typography>
                          </TableCell>
                          <TableCell align="center">
                            <IconButton
                              size="small"
                              onClick={() => playAudio(recording.audio_path)}
                              color={audioPlaying === recording.audio_path ? 'primary' : 'default'}
                            >
                              {audioPlaying === recording.audio_path ? <Pause /> : <PlayArrow />}
                            </IconButton>
                          </TableCell>
                          <TableCell align="center">
                            {recording.labeled ? (
                              <Chip label="Labeled" color="success" size="small" />
                            ) : (
                              <Chip label="Unlabeled" color="warning" size="small" />
                            )}
                          </TableCell>
                          <TableCell align="center">
                            {recording.score !== null ? (
                              <Chip 
                                label={recording.score.toFixed(1)} 
                                color={getScoreColor(recording.score)} 
                                size="small"
                              />
                            ) : (
                              '-'
                            )}
                          </TableCell>
                          <TableCell align="center">
                            <Typography variant="caption">
                              {recording.evaluator || '-'}
                            </Typography>
                          </TableCell>
                          <TableCell align="center">
                            <Button
                              size="small"
                              variant={recording.labeled ? 'outlined' : 'contained'}
                              onClick={() => openLabelDialog(recording)}
                            >
                              {recording.labeled ? 'Edit' : 'Label'}
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>

      {/* Label Dialog */}
      <Dialog open={labelDialogOpen} onClose={() => setLabelDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Label Recording: {currentRecording?.word}
        </DialogTitle>
        <DialogContent>
          {currentRecording && (
            <Box sx={{ pt: 2 }}>
              {/* Audio Player */}
              <Box sx={{ mb: 3, p: 2, bgcolor: 'background.default', borderRadius: 1, textAlign: 'center' }}>
                <Typography variant="body2" gutterBottom>
                  Listen to recording:
                </Typography>
                <IconButton
                  onClick={() => playAudio(currentRecording.audio_path)}
                  color="primary"
                  size="large"
                >
                  {audioPlaying === currentRecording.audio_path ? <Pause fontSize="large" /> : <PlayArrow fontSize="large" />}
                </IconButton>
              </Box>

              {/* Score Slider */}
              <Box sx={{ mb: 3 }}>
                <Typography gutterBottom>
                  Pronunciation Score: {score}/100
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <TextField
                    type="number"
                    value={score}
                    onChange={(e) => setScore(Math.max(0, Math.min(100, Number(e.target.value))))}
                    inputProps={{ min: 0, max: 100, step: 0.5 }}
                    sx={{ width: 100 }}
                  />
                  <input
                    type="range"
                    min="0"
                    max="100"
                    step="0.5"
                    value={score}
                    onChange={(e) => setScore(Number(e.target.value))}
                    style={{ flexGrow: 1 }}
                  />
                </Box>
                <Typography variant="caption" color="text.secondary">
                  90-100: Excellent | 80-89: Good | 70-79: Fair | 60-69: Poor | 0-59: Very Poor
                </Typography>
              </Box>

              {/* Quality Rating */}
              <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel>Overall Quality</InputLabel>
                <Select
                  value={quality}
                  onChange={(e) => setQuality(e.target.value)}
                  label="Overall Quality"
                >
                  <MenuItem value="excellent">Excellent (Native-like)</MenuItem>
                  <MenuItem value="good">Good (Clear, understandable)</MenuItem>
                  <MenuItem value="fair">Fair (Some errors)</MenuItem>
                  <MenuItem value="poor">Poor (Many errors)</MenuItem>
                </Select>
              </FormControl>

              {/* Evaluator Name */}
              <TextField
                fullWidth
                label="Your Name (Evaluator)"
                value={evaluator}
                onChange={(e) => setEvaluator(e.target.value)}
                sx={{ mb: 3 }}
                required
              />

              {/* Notes */}
              <TextField
                fullWidth
                label="Notes (optional)"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                multiline
                rows={4}
                placeholder="Add any observations about pronunciation quality, specific issues, accent, etc."
              />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setLabelDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={saveLabel} 
            variant="contained" 
            disabled={!evaluator.trim()}
          >
            Save Label
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default ReviewPage;
