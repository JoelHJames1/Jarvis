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
import dotenv from 'dotenv';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { solarizedlight } from 'react-syntax-highlighter/dist/esm/styles/prism';

dotenv.config();

const useStyles = makeStyles((theme) => ({
  // ...styles definition
  container: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  chatHistory: {
    height: '70vh',
    overflowY: 'scroll',
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
    padding: theme.spacing(2),
    border: '1px solid lightgray',
    borderRadius: theme.shape.borderRadius,
  },
  codeBlock: {
    backgroundColor: '#f5f5f5',
    padding: theme.spacing(2),
    borderRadius: theme.shape.borderRadius,
  },
}));

function App() {
  const classes = useStyles();
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isWaitingResponse, setIsWaitingResponse] = useState(false);
  const chatHistoryRef = useRef(null);

  const formatCodeBlock = (text) => {
    const codeRegex = /```[\s\S]*?\n([\s\S]*?)```/g;
    let match;
    let isCode = false;

    while ((match = codeRegex.exec(text)) !== null) {
      isCode = true;
      text = text.replace(match[0], "").trim();
    }

    return isCode;
  };

  useEffect(() => {
    if (answer) {
      const timer = setTimeout(() => {
        setChatHistory((prevChatHistory) => [
          ...prevChatHistory,
          { from: 'Jarvis', text: answer, isCode: formatCodeBlock(answer) },
        ]);
        setAnswer('');
        // ...synthesizeSpeech function and API call omitted for brevity

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
            {chat.isCode ? (
              <SyntaxHighlighter language="csharp" style={solarizedlight} className={classes.codeBlock}>
                {chat.text}
              </SyntaxHighlighter>
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
