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

const ENCRYPT_SERVER_ADDRESS_REST = process.env.ENCRYPT_SERVER_ADDRESS_REST;
const DECRYPT_SERVER_ADDRESS_REST = process.env.DECRYPT_SERVER_ADDRESS_REST;

const encryptClient = new cryptoPackage.CryptoService(
    process.env.ENCRYPT_SERVER_ADDRESS,
    grpc.credentials.createInsecure()
);

const decryptClient = new cryptoPackage.CryptoService(
    process.env.DECRYPT_SERVER_ADDRESS,
    grpc.credentials.createInsecure()
);

app.post("/encrypt/", (req, res) => {
    const { text, key } = req.body;

    encryptClient.Encrypt({ text, key }, (err, response) => {
        if (err) {
            console.error("Erro na codificação:", err);
            return res.status(500).json({ error: err.message });
        }
        res.json({ result: response.result });
    });
});

app.post("/decrypt/", (req, res) => {
    const { text, key } = req.body;

    decryptClient.Decrypt({ text, key }, (err, response) => {
        if (err) {
            console.error("Erro na decodificação:", err);
            return res.status(500).json({ error: err.message });
        }
        res.json({ result: response.result });
    });
});


app.post("/encrypt_rest/", async (req, res) => {
    const { text, key } = req.body;
    try {
        const response = await axios.post("http://"+ENCRYPT_SERVER_ADDRESS_REST+"/encrypt", {
            text: text,
            key: key
        });
        res.json({ result: response.data.result });
    } catch (error) {
        console.error("Erro na codificação:", error.message);
        res.status(500).json({ error: "Erro ao codificar texto." });
    }
});

app.post("/decrypt_rest/", async (req, res) => {
    const { text, key } = req.body;

    try {
        const response = await axios.post("http://"+DECRYPT_SERVER_ADDRESS_REST+"/decrypt", {
            text: text,
            key: key
        });
        res.json({ result: response.data.result });
    } catch (error) {
        console.error("Erro na decodificação:", error.message);
        res.status(500).json({ error: "Erro ao decodificar texto." });
    }
});


app.listen(process.env.PORT, () => {
    console.log(`API Gateway running on http://0.0.0.0:${process.env.PORT}`);
});
