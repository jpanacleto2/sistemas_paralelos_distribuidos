import services from "./sevices";

export class GatewayServices {
    encriptWords = async (plaintext, key) => {
        const response = await services.post('/encrypt/', {plaintext: plaintext, key: key})
        return response.data
    }

    decriptWords = async (ciphertext, key) => {
        const response = await services.post('/decrypt/', {ciphertext: ciphertext, key: key})
        return response.data
    }
}