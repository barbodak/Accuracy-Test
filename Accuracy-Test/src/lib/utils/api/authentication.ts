import axios from 'axios';
import { BASE_API_URL, COOKIE_MAX_AGE } from "$lib/utils/constants";
import { goto } from '$app/navigation';
import { retreiveAccount, retreiveQuiz } from "$lib/utils/api/quiz-apis";
import { setCookies, deleteCookies } from "$lib/utils/cookies";

export const login = async (data: object) => {
    try {
        const url = `${BASE_API_URL}/login/`;
        const response = await axios({
            method: 'post',
            url: url,
            data: data,
        });

        console.log(response.data.token);

        if (response.data?.token) {
            setCookies('auth_token', response.data.token, COOKIE_MAX_AGE);
        }
        const account = await retreiveAccount();

        console.log(account.first_name);

        if (account.is_final === false) {
            goto('/Login/Finalize');
        } else {
            goto('/');
        }
    } catch (e) {
        console.error("Login failed:", e);
    }
};

export const signup = async (data: object) => {
    try {
        const url = `${BASE_API_URL}/account/signup/`;
        const response = await axios({
            method: 'post',
            url: url,
            data: data,
        });

        if (response.data?.token) {
            setCookies('auth_token', response.data.token, COOKIE_MAX_AGE);
        }

        const account = await retreiveAccount();
        return response.data;
    } catch (e) {
        console.error("Signup failed:", e);
        throw e;
    }

}



export const logout = () => {
    deleteCookies('auth_token');
    goto('/Login'); // Redirect to the login page
};

