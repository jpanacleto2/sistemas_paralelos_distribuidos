const express = require("express");
const cors = require("cors");
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");

const app = express();
app.use(cors());
app.use(express.json());

const PROTO_PATH = "./crypto.proto";
const ENCRYPT_SERVER_ADDRESS = "localhost:50051"; // Servidor de codificação
const DECRYPT_SERVER_ADDRESS = "localhost:50052"; // Servidor de decodificação

// Carrega o arquivo .proto
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
});

const cryptoProto = grpc.loadPackageDefinition(packageDefinition).crypto;

const encryptClient = new cryptoProto.CryptoService(
    ENCRYPT_SERVER_ADDRESS,
    grpc.credentials.createInsecure()
);

const decryptClient = new cryptoProto.CryptoService(
    DECRYPT_SERVER_ADDRESS,
    grpc.credentials.createInsecure()
);

app.post("/encrypt", (req, res) => {
    const { plaintext, key } = req.body;
    
    encryptClient.Encrypt({ plaintext, key }, (err, response) => {
        if (err) {
            console.error("Erro na codificação:", err);
            return res.status(500).json({ error: err.message });
        }
        res.json({ ciphertext: response.ciphertext });
    });
});

app.post("/decrypt", (req, res) => {
    const { ciphertext, key } = req.body;
    
    decryptClient.Decrypt({ ciphertext, key }, (err, response) => {
        if (err) {
            console.error("Erro na decodificação:", err);
            return res.status(500).json({ error: err.message });
        }
        res.json({ plaintext: response.plaintext });
    });
});

const PORT = 8080;
app.listen(PORT, () => {
    console.log(`API Gateway running on http://0.0.0.0:${PORT}`);
});