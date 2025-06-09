import { useState, useRef } from "react";

export default function AnswerEnter() {
    const [answer, setAnswer] = useState("");
    const [showVideo, setShowVideo] = useState(false);
    const [isMuted, setIsMuted] = useState(true);
    const videoRef = useRef(null);

    const checkAnswer = (e) => {
        e.preventDefault();
        if (answer !== "09031993") {
            setShowVideo(true);
        } else {
            alert("Как ты угадала? -_-");
        }
    };

    const handleVideoEnd = () => {
        setShowVideo(false);
        setIsMuted(true);
        alert("Подсказка: день рождение не твое, а твоего главного биаса, хахаха");
        // Сбрасываем звук для следующего воспроизведения
    };

    const handleVideoClick = () => {
        if (videoRef.current) {
            videoRef.current.muted = false;
            setIsMuted(false);
        }
    };

    return (
        <>
            <div className="answer">
                <h1>Подтвердите свою личность...</h1>
                <p>Введите дату рождения:</p>
                <form onSubmit={checkAnswer}>
                    <input
                        className="answer"
                        value={answer}
                        onChange={(e) => setAnswer(e.target.value)}
                    />
                    <button type="submit">Проверить</button>
                </form>
            </div>

            {showVideo && (
                <div
                    className="video-overlay"
                    onClick={handleVideoClick}
                    style={{
                        position: "fixed",
                        top: 0,
                        left: 0,
                        width: "100vw",
                        height: "100vh",
                        backgroundColor: "black",
                        zIndex: 1000,
                        cursor: "pointer",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center"
                    }}
                >
                    <video
                        ref={videoRef}
                        autoPlay
                        muted={isMuted}
                        playsInline
                        onEnded={handleVideoEnd}
                        style={{
                            width: "100%",
                            height: "100%",
                            objectFit: "contain"
                        }}
                    >
                        <source src="./../../public/error.mp4" type="video/mp4" />
                    </video>
                    {isMuted && (
                        <div style={{
                            position: "absolute",
                            bottom: "20px",
                            color: "white",
                            fontSize: "18px"
                        }}>
                            🔇 Кликните по видео, чтобы включить звук
                        </div>
                    )}
                </div>
            )}
        </>
    );
}
