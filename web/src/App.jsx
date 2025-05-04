import React, { useState, useCallback, useMemo } from 'react';
import './App.css';
import { GatewayServices } from "./Services/GatewayServices";

function App() {
    const gatewayServices = useMemo(() => new GatewayServices(), []);
    const [text, setText] = useState("");
    const [key, setKey] = useState("");
    const [resultText, setResultText] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    
    const handleOperation = useCallback(async (operation) => {
        if (!text || !key) {
            setError("Por favor, preencha tanto o texto quanto a chave");
            return;
        }
        
        setIsLoading(true);
        setError(null);
        setResultText("");
        
        try {
            const result = operation === 'encrypt' 
                ? await gatewayServices.encriptWords(text, key)
                : await gatewayServices.decriptWords(text, key);
            setResultText(result);
        } catch (err) {
            setError("Ocorreu um erro ao processar sua solicitação.");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    }, [text, key, gatewayServices]);

    const handleEncrypt = () => handleOperation('encrypt');
    const handleDecrypt = () => handleOperation('decrypt');

    return (
        <div className="app-container">
            <h1>Cifra de Vigenère</h1>

            <div className="input-section">
                <p>Digite um texto:</p>
                <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Insira o texto aqui"
                    disabled={isLoading}
                />
                
                <p>Digite uma chave:</p>
                <input
                    type="text"
                    value={key}
                    onChange={(e) => setKey(e.target.value)}
                    placeholder="Insira a chave aqui"
                    disabled={isLoading}
                />
                
                <div className="button-group">
                    <button 
                        onClick={handleEncrypt}
                        disabled={isLoading || !text || !key}
                        className="action-button encrypt-button"
                    >
                        {isLoading ? (
                            <>
                                <span className="loading-spinner"></span>
                                Processando...
                            </>
                        ) : 'Criptografar'}
                    </button>
                    <button 
                        onClick={handleDecrypt}
                        disabled={isLoading || !text || !key}
                        className="action-button decrypt-button"
                    >
                        {isLoading ? (
                            <>
                                <span className="loading-spinner"></span>
                                Processando...
                            </>
                        ) : 'Descriptografar'}
                    </button>
                </div>
            </div>

            {error && <div className="error">{error}</div>}

            <div className="result-section">
                <h2>Resultado:</h2>
                <div className="result-box">
                    {resultText || <span className="placeholder">O resultado aparecerá aqui</span>}
                </div>
            </div>
        </div>
    );
}

export default App;