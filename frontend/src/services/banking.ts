import axios from "axios";

const API_URL = 'http://127.0.0.1:5000';

export interface BackendResponse {
    message: string;
}

export interface ResourceResponse<I> extends BackendResponse {
    data: I
}

export interface HistoryResponse {
    id: number,
    amount: number,
    action: string,
    time: string
}

export async function getHistory() {
    return await axios.get<ResourceResponse<HistoryResponse[]>>(API_URL + '/history', {
        headers: {
            'Accept': 'application/json'
        }
    });
}

export interface BalanceResponse {
    balance: string
}

export async function getBalance() {
    return await axios.get<ResourceResponse<BalanceResponse>>(API_URL + '/balance', {
        headers: {
            'Accept': 'application/json'
        }
    })
}

export async function deposit(amount: string, idempotenceKey: string) {
    return await axios.post<BackendResponse>(API_URL + '/deposit', {
        amount
    }, {
        headers: {
            'Accept': 'application/json',
            'Idempotency-Key': idempotenceKey
        }
    });
}

export async function withdraw(amount: string, idempotenceKey: string) {
    return await axios.post<BackendResponse>(API_URL + '/withdraw', {
        amount
    }, {
        headers: {
            'Accept': 'application/json',
            'Idempotency-Key': idempotenceKey
        }
    });
}

export default {
    getHistory,
    getBalance,
    deposit,
    withdraw
}