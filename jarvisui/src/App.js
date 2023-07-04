import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Avatar from '@material-ui/core/Avatar';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import JarvisAvatar from './Avatar/Jarvis.png';
import UserAvatar from './Avatar/Joel.png';

const useStyles = makeStyles((theme) => ({
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
    width: theme.spacing(7),
    height: theme.spacing(7),
  },
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
  },
  chatHistory: {
    width: '100%',
    maxHeight: '70vh',
    overflowY: 'scroll',
    marginBottom: theme.spacing(2),
  },
  codeBlock: {
    fontFamily: 'monospace',
    backgroundColor: '#2f2f2f',
    padding: theme.spacing(1),
    margin: theme.spacing(1),
    borderRadius: theme.spacing(1),
    color: '#ffffff',
  },
}));

function App() {
  const classes = useStyles();
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isWaitingResponse, setIsWaitingResponse] = useState(false);
  const chatHistoryRef = useRef(null); // Ref for chat history container

  useEffect(() => {
    if (answer) {
      const timer = setTimeout(() => {
        setChatHistory((prevChatHistory) => [
          ...prevChatHistory,
          { from: 'Jarvis', text: answer },
        ]);
        setAnswer('');
      }, 500);

      return () => clearTimeout(timer);
    }
  }, [answer]);

  const askQuestion = async () => {
    setIsWaitingResponse(true);
    setChatHistory((prevChatHistory) => [
      ...prevChatHistory,
      { from: 'User', text: question },
    ]);
    setQuestion('');

    try {
      const response = await axios.post('http://localhost:5000/ask', { question });
      console.log(response.data);
      setAnswer(response.data.response);
    } catch (err) {
      console.error(err);
    }
    setIsWaitingResponse(false);
  };

  useEffect(() => {
    chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
  }, [chatHistory]);

  return (
    <Container className={classes.container} maxWidth="md">
      <div className={classes.chatHistory} ref={chatHistoryRef}>
        {chatHistory.map((chat, index) => (
          <div key={index}>
            <Avatar
              alt={chat.from + ' Avatar'}
              src={chat.from === 'Jarvis' ? JarvisAvatar : UserAvatar}
              className={classes.avatar}
            />
            <Typography component="h1" variant="h5">
              {chat.from}:
            </Typography>
            {chat.from === 'Jarvis' && chat.text.startsWith('using') ? (
              <pre className={classes.codeBlock}>{chat.text}</pre>
            ) : (
              <Typography variant="body1">{chat.text}</Typography>
            )}
          </div>
        ))}
      </div>
      <TextField
        variant="outlined"
        margin="normal"
        required
        fullWidth
        id="question"
        label="Question"
        name="question"
        autoFocus
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        disabled={isWaitingResponse}
        onKeyPress={(e) => {
          if (e.key === 'Enter') {
            askQuestion();
          }
        }}
      />
      <Button
        type="submit"
        variant="contained"
        color="primary"
        onClick={askQuestion}
        disabled={isWaitingResponse}
      >
        Ask
      </Button>
    </Container>
  );
}

export default App;
