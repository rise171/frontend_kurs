import React, { useState, useEffect, useRef } from 'react';
import { Loader } from "rsuite";
import './Loading.css';

const LoadingComponent = ({ duration, onLoadingComplete }) => {
    const [isLoading, setIsLoading] = useState(true);
    const [isMuted, setIsMuted] = useState(true); // Начинаем с muted
    const videoRef = useRef(null);

    useEffect(() => {
        const timer = setTimeout(() => {
            setIsLoading(false);
            if (onLoadingComplete) onLoadingComplete();
        }, duration);

        return () => clearTimeout(timer);
    }, [duration, onLoadingComplete]);

    const handleClick = () => {
        if (videoRef.current) {
            videoRef.current.muted = false; // Включаем звук
            setIsMuted(false);
        }
    };

    if (!isLoading) return null;

    return (
        <div
            onClick={handleClick}// Курсор как указатель, чтобы показать, что можно кликнуть
        >
            <div className="loading-content">
                <video
                    ref={videoRef}
                    autoPlay
                    loop
                    muted={isMuted} // Управляем звуком через состояние
                    playsInline // Важно для iOS
                    width="50%"
                >
                    <source src="./../../public/loading-video.mp4" type="video/mp4" />
                    Ваш браузер не поддерживает видео.
                </video>
                <p>Use headphones for good experience =)</p>
                {isMuted && (
                    <p style={{ color: 'white', marginTop: '10px' }}>
                        🔇
                    </p>
                )}
                <Loader content="Загрузка..." vertical />
            </div>
        </div>
    );
};

export default LoadingComponent;

