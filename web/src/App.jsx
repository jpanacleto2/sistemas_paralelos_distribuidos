import React, { useState, useCallback } from 'react';
import './App.css';
import { GatewayServices } from "./Services/GatewayServices";

function App() {
    const gatewayServices = new GatewayServices();
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
        
        try {
            const result = operation === 'encrypt' 
                ? await gatewayServices.encriptWords(text, key)
                : await gatewayServices.decriptWords(text, key);
            setResultText(result);
        } catch (err) {
            setError("Ocorreu um erro ao processar sua requisição");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    }, [text, key, gatewayServices]);

    const handleEncrypt = () => handleOperation('encrypt');
    const handleDecrypt = () => handleOperation('decrypt');

    return (
        <div>
            <h1>Cifra de Vigenère</h1>

            <div>
                <p>Digite um texto:</p>
                <textarea
                    type="text"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Insira o texto aqui"
                />
                
                <p>Digite uma chave:</p>
                <input
                    type="text"
                    value={key}
                    onChange={(e) => setKey(e.target.value)}
                    placeholder="Insira a chave aqui"
                />
                
                <div className="button-group">
                    <button 
                        onClick={handleEncrypt}
                        disabled={isLoading || !text || !key}
                        className="action-button encrypt-button"
                    >
                        {isLoading ? 'Processando...' : 'Criptografar'}
                    </button>
                    <button 
                        onClick={handleDecrypt}
                        disabled={isLoading || !text || !key}
                        className="action-button decrypt-button"
                    >
                        {isLoading ? 'Processando...' : 'Descriptografar'}
                    </button>
                </div>
            </div>

            {error && <div>{error}</div>}

            <div>
                <h2>Resultado:</h2>
                <div>
                    {resultText || <span className="placeholder">O resultado aparecerá aqui</span>}
                </div>
            </div>
        </div>
    );
}

export default App;