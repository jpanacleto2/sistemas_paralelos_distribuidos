const express = require("express");
const cors = require("cors");
const axios = require("axios");
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");
const dotenv = require("dotenv");

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const PROTO_PATH = "../shared/crypto.proto";

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
});

const cryptoPackage = grpc.loadPackageDefinition(packageDefinition).crypto;

const encryptClient = new cryptoPackage.CryptoService(
    process.env.ENCRYPT_SERVER_ADDRESS,
    grpc.credentials.createInsecure()
);

const decryptClient = new cryptoPackage.CryptoService(
    process.env.DECRYPT_SERVER_ADDRESS,
    grpc.credentials.createInsecure()
);

app.post("/encrypt", (req, res) => {
    const { text, key } = req.body;

    encryptClient.Encrypt({ text, key }, (err, response) => {
        if (err) {
            console.error("Erro na codificação:", err);
            return res.status(500).json({ error: err.message });
        }
        res.json({ result: response.result });
    });
});

app.post("/decrypt", (req, res) => {
    const { text, key } = req.body;

    decryptClient.Decrypt({ text, key }, (err, response) => {
        if (err) {
            console.error("Erro na decodificação:", err);
            return res.status(500).json({ error: err.message });
        }
        res.json({ result: response.result });
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
