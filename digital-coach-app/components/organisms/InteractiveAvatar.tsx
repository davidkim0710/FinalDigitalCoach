import {
  forwardRef,
  useImperativeHandle,
  useEffect,
  useRef,
  useState,
} from "react";
import type { StartAvatarResponse } from "@heygen/streaming-avatar";
import StreamingAvatar, {
  AvatarQuality,
  StreamingEvents,
  TaskMode,
  TaskType,
} from "@heygen/streaming-avatar";
import styles from "@App/styles/NaturalConversationPage.module.scss";
import OpenAIAssistant, { OpenAIAssistantHandle } from "./OpenAssistant"; // Import type

const openaiApiKey = process.env.OPEN_AI_API_KEY;

const InteractiveAvatar = forwardRef((props, ref) => {
  const [isLoadingSession, setIsLoadingSession] = useState(false);
  const [isLoadingRepeat, setIsLoadingRepeat] = useState(false);
  const [stream, setStream] = useState<MediaStream>();
  const [debug, setDebug] = useState<string>("");
  const [knowledgeId, setKnowledgeId] = useState<string>("");
  const [avatarId, setAvatarId] = useState<string>("");
  const [language, setLanguage] = useState<string>("en");
  const [data, setData] = useState<StartAvatarResponse>();
  // 'UserTextRef' holds the candidate's final answer that triggers the interviewer prompt.
  const UserTextRef = useRef("");
  const [text, setText] = useState<string>("");
  const mediaStream = useRef<HTMLVideoElement>(null);
  const avatar = useRef<StreamingAvatar | null>(null);
  const [chatMode, setChatMode] = useState("text_mode");
  const [isUserTalking, setIsUserTalking] = useState(false);
  const [response, setResponse] = useState<string>("");
  const openAIRef = useRef<OpenAIAssistantHandle | null>(null);
  let counter = 0;
  async function fetchAccessToken() {
    try {
      const apiKey =
        "M2NlNTQ2NzZhOGYxNGRkYWFkYjZiNGUxZTFkY2I0NGItMTczOTU2NTAzNg==";
      const response = await fetch(
        "https://api.heygen.com/v1/streaming.create_token",
        {
          method: "POST",
          headers: { "x-api-key": apiKey },
        }
      );
      const { data } = await response.json();
      console.log("Access Token:", data.token);
      return data.token;
    } catch (error) {
      console.error("Error fetching access token:", error);
    }
    return "";
  }

  async function startSession() {
    setIsLoadingSession(true);
    const newToken = await fetchAccessToken();
    avatar.current = new StreamingAvatar({
      token: newToken,
    });

    avatar.current.on(StreamingEvents.STREAM_READY, (event) => {
      console.log("Stream ready:", event.detail);
      setStream(event.detail);
    });

    avatar.current.on(StreamingEvents.AVATAR_START_TALKING, (e) => {
      console.log("Avatar started talking", e);
    });

    avatar.current.on(StreamingEvents.AVATAR_TALKING_MESSAGE, (message) => {
      console.log("Avatar talking message:", message);
    });
    // Update 'UserTextRef' with the user's spoken message as it is transcribed.
    avatar.current.on(StreamingEvents.USER_TALKING_MESSAGE, (message) => {
      console.log("User talking message:", message);
      UserTextRef.current = message.detail.message;
      console.log(UserTextRef.current);
      handleSpeak(); // <-- Moved here
    });

    try {
      const res = await avatar.current.createStartAvatar({
        quality: AvatarQuality.Low,
        avatarName: "default",
        disableIdleTimeout: true,
      });
      setData(res);
      // Start voice chat with silence prompt enabled to disable default responses.
      await avatar.current?.startVoiceChat({
        useSilencePrompt: true,
      });
    } catch (error) {
      console.error("Error starting avatar session:", error);
    } finally {
      setIsLoadingSession(false);
    }

    // Call handleSpeak() when the user stops talking, instead of AVATAR_STOP_TALKING.
    avatar.current?.on(StreamingEvents.USER_STOP, (event) => {
      console.log(">>>>> User stopped talking:", event);
      avatar.current?.interrupt();
      console.log(UserTextRef.current);
    });

    // We remove the handleSpeak() call here to prevent the infinite loop
    avatar.current.on(StreamingEvents.AVATAR_STOP_TALKING, (e) => {
      console.log("Avatar stopped talking", e);
      // NO handleSpeak() here
    });

    avatar.current.on(StreamingEvents.STREAM_DISCONNECTED, () => {
      console.log("Stream disconnected");
      endSession();
    });

    // Second STREAM_READY event (if needed)
    avatar.current?.on(StreamingEvents.STREAM_READY, (event) => {
      console.log(">>>>> Stream ready:", event.detail);
      setStream(event.detail);
    });

    // When the user starts talking, we set the flag.
    avatar.current?.on(StreamingEvents.USER_START, (event) => {
      console.log(">>>>> User started talking:", event);
      setIsUserTalking(true);
    });
  }

  async function handleSpeak() {
    setIsLoadingRepeat(true);
    if (!avatar.current) {
      setDebug("Avatar API not initialized");
      return;
    }

    // In-depth interviewer prompt that instructs the assistant how to behave:
    const interviewerPrompt = `You are a professional job interviewer. Your responsibilities include:
    - Evaluating the candidate's skills, experience, and overall fit for the role.
    - Asking clarifying questions to understand the candidate's perspective.
    - Encouraging the candidate to elaborate on their experiences with specific examples.
    - Maintaining a friendly, respectful, and professional tone at all times.
    - Adjusting your follow-up questions based on the candidate's previous answers.

Based on the candidate's answer provided below, please ask a relevant and probing follow-up question to gather deeper insights.

Candidate Answer: `;
    const promptText = interviewerPrompt + UserTextRef.current;
    console.log(promptText);

    if (openAIRef.current) {
      const response = await openAIRef.current.sendMessage(promptText);
      console.log("OpenAI Response:", response);
      setResponse(response);
      await avatar.current
        .speak({
          text: response,
          taskType: TaskType.REPEAT,
          taskMode: TaskMode.SYNC,
        })
        .catch((e) => {
          setDebug(e.message);
        });
      setIsLoadingRepeat(false);
    }
  }

  async function handleInterrupt() {
    if (!avatar.current) {
      setDebug("Avatar API not initialized");
      return;
    }
    await avatar.current.interrupt().catch((e) => {
      setDebug(e.message);
    });
  }

  async function endSession() {
    await avatar.current?.stopAvatar();
    setStream(undefined);
  }

  useImperativeHandle(ref, () => ({
    startSession,
    endSession,
    handleInterrupt,
  }));

  useEffect(() => {
    // Start/stop listening based on whether text is present.
    if (text) {
      avatar.current?.startListening();
    } else {
      avatar.current?.stopListening();
    }
  }, [text]);

  useEffect(() => {
    // Cleanup on unmount
    return () => {
      endSession();
    };
  }, []);

  useEffect(() => {
    if (stream && mediaStream.current) {
      mediaStream.current.srcObject = stream;
      mediaStream.current.onloadedmetadata = () => {
        mediaStream.current!.play();
        setDebug("Playing");
      };
    }
  }, [mediaStream, stream]);

  return (
    <div className={styles.avatarContainer}>
      <OpenAIAssistant ref={openAIRef} />
      {!stream ? (
        <img src="/avatar.png" className="fixed-size-image" alt="Avatar" />
      ) : (
        <video
          ref={mediaStream}
          autoPlay
          playsInline
          style={{
            width: "500px",
            height: "300px",
            objectFit: "contain",
          }}
        >
          <track kind="captions" />
        </video>
      )}
    </div>
  );
});

export default InteractiveAvatar;
