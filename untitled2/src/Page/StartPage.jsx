import { useState, useEffect } from 'react';
import LoadingComponent from './../Components/Loading.jsx';
import AnswerEnter from "../Components/AnswerEnter.jsx";

const StartPage = () => {
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setIsLoading(false);
        }, 10000); // 10 секунд загрузки

        return () => clearTimeout(timer);
    }, []);

    return (
        <div className="page">
            {isLoading ? (
                <LoadingComponent duration={10000} />
            ) : (
                <AnswerEnter />
            )}
        </div>
    );
};

export default StartPage;