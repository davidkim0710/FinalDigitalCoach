import { useState, useEffect, useRef } from "react";
import Card from "@App/components/atoms/Card";
import AuthGuard from "@App/lib/auth/AuthGuard";
import { useReactMediaRecorder } from "react-media-recorder";
import StorageService from "@App/lib/storage/StorageService";
import { v4 as uuidv4 } from "uuid";
import styles from "@App/styles/NaturalConversationPage.module.scss";
import axios from "axios";
import InteractiveAvatar from "@App/components/organisms/InteractiveAvatar";

export default function NaturalConversationPage() {
  const avatarRef = useRef<{
    startSession: () => void;
    endSession: () => void;
    handleInterrupt: () => void;
  } | null>(null);

  const handleStartInterview = async () => {
    if (wasRecording) {
      stopRecording();
      await avatarRef.current?.endSession(); // Start avatar session
      setWasRecording(false);
    } else {
      setWasRecording(true);
      await avatarRef.current?.startSession(); // Start avatar session
      startRecording();
    }
  };

  const handleInterruptAvatar = async () => {
    await avatarRef.current?.handleInterrupt(); // Start avatar session
  };

  const [wasRecording, setWasRecording] = useState<any>(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const { status, startRecording, stopRecording, mediaBlobUrl, previewStream } =
    useReactMediaRecorder({ video: true });

  const [responses, setResponses] = useState<
    { timestamp: string; text: string }[]
  >([]);

  const getResponse = async () => {
    try {
      //Get the recording file
      const getFile = async () => {
        const url = mediaBlobUrl || "/output.mp4"; // Fallback URL if mediaBlobUrl is not available
        let blob = await fetch(url).then((res) => res.blob());
        return new File([blob], "video.mp4");
      };
      const file = await getFile();

      //Upload video to storage
      const url = (await StorageService.uploadAnswerVideo(
        file,
        uuidv4()
      )) as any;
      const dlURL = await StorageService.getDownloadUrlFromVideoUrlRef(
        "gs://" + url.ref._location.bucket + "/" + url.ref._location.path
      );
      console.log(dlURL);
      //Send video URL for processing
      const sentResponse = await axios.post("http://localhost:8000/predict", {
        videoUrl: dlURL,
      });
      const jobId = sentResponse.data.message.split(" ")[1]; // Extract jobId

      // Wait for processing results
      const resultResponse = await axios.get(
        `http://localhost:8000/results/${jobId}`
      );

      if (resultResponse.data.result) {
        console.log(resultResponse.data.result);
        const newResponse = {
          timestamp: `[${new Date().toLocaleString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false, // 24-hour format
          })}]`,
          text: resultResponse.data.result.text_analysis.output_text.replace(
            /(\.)(?=\S)/g,
            "$1 "
          ), //add a space after each period
        };
        setResponses((prevResponses) => [...prevResponses, newResponse]);
      } else {
        alert("Results not ready. Try again later.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while processing the recording.");
    }
  };

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.srcObject = previewStream || null;
    }
  }, [previewStream]);

  return (
    <AuthGuard>
      <div>
        <div className={styles.videoContainer}>
          <div className={styles.videoBox}>
            <video
              ref={videoRef}
              controls
              autoPlay
              style={{
                width: "300px",
                height: "200px",
                objectFit: "contain",
              }}
            />
            <InteractiveAvatar ref={avatarRef} />
            <Card title="Transcript">
              {responses.length > 0 ? (
                responses.map((response, index) => (
                  <div key={index}>
                    <p>
                      <strong>{response.timestamp} User:</strong>
                    </p>
                    <p>{response.text}</p>
                  </div>
                ))
              ) : (
                <p>No transcript available.</p>
              )}
            </Card>
          </div>
        </div>
        <div className={styles.buttonBox}>
          <button
            className={styles.recordButton}
            onClick={handleStartInterview}
          >
            {wasRecording ? "Stop Interview" : "Start Interview"}
          </button>
          <button className={styles.saveButton} onClick={getResponse}>
            Test
          </button>
          <button onClick={handleInterruptAvatar}>Interrupt Task</button>
          {mediaBlobUrl && (
            <button className={styles.saveButton} onClick={getResponse}>
              GetResponse
            </button>
          )}
        </div>
      </div>
    </AuthGuard>
  );
}
