import React, { useState } from 'react';
import axios from 'axios';
import { Container, Box, Button, Typography, Paper } from '@mui/material';

function App() {
  const [files, setFiles] = useState([]);
  const [summary, setSummary] = useState("");

  const handleFileChange = (e) => {
    setFiles([...files, ...Array.from(e.target.files)]);
  };

  const handleSummarize = async () => {
    if (files.length === 0) {
      alert("Please select at least one document.");
      return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }

    try {
      const response = await axios.post('http://localhost:5004/summarize', formData);
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error summarizing documents:', error);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          PDF-Document Summarization
        </Typography>
        <Box sx={{ my: 2 }}>
          <input
            type="file"
            multiple
            onChange={handleFileChange}
            style={{ margin: '10px 0' }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleSummarize}
            sx={{ mt: 2 }}
          >
            Summarize
          </Button>
        </Box>
        <Box sx={{ my: 2 }}>
          <Typography variant="h5" component="h2" gutterBottom>
            Summary
          </Typography>
          <Paper elevation={3} sx={{ p: 2, minHeight: '200px', backgroundColor: '#f5f5f5' }}>
            <Typography variant="body1" component="p">
              {summary || "Your summary will appear here..."}
            </Typography>
          </Paper>
        </Box>
      </Box>
    </Container>
  );
}

export default App;
