const express = require("express");
const cors = require("cors");
const axios = require("axios");
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");


const app = express();
app.use(cors());
app.use(express.json());
require("dotenv").config();

const PROTO_PATH = "../shared/crypto.proto";

const ENCRYPT_SERVER_ADDRESS = process.env.ENCRYPT_SERVER_ADDRESS;
const DECRYPT_SERVER_ADDRESS = process.env.DECRYPT_SERVER_ADDRESS;

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
});

const cryptoProto = grpc.loadPackageDefinition(packageDefinition).crypto;

const encryptClient = new cryptoProto.CryptoService(
    process.env.ENCRYPT_SERVER_ADDRESS,
    grpc.credentials.createInsecure()
);

const decryptClient = new cryptoProto.CryptoService(
    process.env.DECRYPT_SERVER_ADDRESS,
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


app.post("/encrypt_rest", async (req, res) => {
    const { plaintext, key } = req.body;

    try {
        const response = await axios.post(ENCRYPT_SERVER_ADDRESS, {
            text: plaintext,
            key: key
        });
        res.json({ ciphertext: response.data.result });
    } catch (error) {
        console.error("Erro na codificação:", error.message);
        res.status(500).json({ error: "Erro ao codificar texto." });
    }
});

app.post("/decrypt_rest", async (req, res) => {
    const { ciphertext, key } = req.body;

    try {
        const response = await axios.post(DECRYPT_SERVER_ADDRESS, {
            text: ciphertext,
            key: key
        });
        res.json({ plaintext: response.data.result });
    } catch (error) {
        console.error("Erro na decodificação:", error.message);
        res.status(500).json({ error: "Erro ao decodificar texto." });
    }
});


app.listen(process.env.PORT, () => {
    console.log(`API Gateway running on http://0.0.0.0:${process.env.PORT}`);
});