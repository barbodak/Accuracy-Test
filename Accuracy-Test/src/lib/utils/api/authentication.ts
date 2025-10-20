import { userData } from "../../stores/userStore";
import axios from 'axios';
import { BASE_API_URL } from "../constants";
import { goto } from '$app/navigation';
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
        goto('/');
        // success('you have successfully logged in');
    } catch (e) {
        console.error("Login failed:", e);
        // failure('login failed check your username and password');
    }
};

export const logout = () => {
    userData.set({}); // Clear user data from the store
    goto('/Login'); // Redirect to the login page
};

