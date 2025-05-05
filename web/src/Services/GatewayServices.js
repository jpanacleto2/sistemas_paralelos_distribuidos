import services from "./sevices";

export class GatewayServices {
    encriptWords = async (plaintext, key) => {
        const response = await services.post('/encrypt/', {text: plaintext, key: key})
        return response.data.result
    }

    decriptWords = async (ciphertext, key) => {
        const response = await services.post('/decrypt/', {text: ciphertext, key: key})
        return response.data.result
    }
}