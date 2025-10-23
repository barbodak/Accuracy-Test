import { userData } from "../../stores/userStore";
import axios from 'axios';
import { BASE_API_URL } from "../constants";
import { goto } from '$app/navigation';
import { retreiveAccount, retreiveQuiz } from "$lib/utils/api/quiz-apis";
// import { success, failure, warning } from "../toasts";

export const login = async (data: object) => {
    try {
        const url = `${BASE_API_URL}/login/`;
        const response = await axios({
            method: 'post',
            url: url,
            data: data,
        });
        userData.set(response.data);
        const account = await retreiveAccount();
        console.log(account);

        if (account.is_final === false) {
            goto('/Login/Finalize');
        } else {
            goto('/');
        }
    } catch (e) {
        console.error("Login failed:", e);
    }
};


export const logout = () => {
    userData.set({}); // Clear user data from the store
    goto('/Login'); // Redirect to the login page
};

