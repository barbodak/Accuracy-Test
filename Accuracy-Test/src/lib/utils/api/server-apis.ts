import { BASE_API_URL } from "$lib/utils/constants";


type ServerFetcher = (input: RequestInfo, init?: RequestInit) => Promise<Response>;

export async function fetchAcount(fetch: ServerFetcher, token: string) {
    const res = await fetch(`${BASE_API_URL}/account/retrieve`, {
        headers: { Authorization: `Token ${token}` }
    });
    if (!res.ok)
        throw new Error(`account ${res.statusText}`);
    return res.json();
}

export async function fetchQuiz(fetch: ServerFetcher, token: string, quiz_type: string) {
    const res = await fetch(`${BASE_API_URL}/quiz/retrieve/${quiz_type}`, {
        headers: { Authorization: `Token ${token}` }
    });
    if (!res.ok)
        throw new Error(`quiz ${quiz_type}: ${res.statusText}`);
    return res.json();
}

export async function fetchQuizAnswer(fetch: ServerFetcher, token: string, quiz_type: string) {
    const res = await fetch(`${BASE_API_URL}/quiz/retrieve/${quiz_type}`, {
        headers: { Authorization: `Token ${token}` }
    });
    if (!res.ok)
        throw new Error(`quiz-anwer ${quiz_type}: ${res.statusText}`);
    return res.json();
}
