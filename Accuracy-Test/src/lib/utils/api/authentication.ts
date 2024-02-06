import { userData } from "../../stores/userStore";
import axios from 'axios';
import { BASE_API_URL } from "../constants";
import { goto } from '$app/navigation';
// import { success, failure, warning } from "../toasts";

export const login = async (data:object) => {
    try {
        const url = `${ BASE_API_URL }/login/`;
        const response = await axios({
            method: 'post',
            url: url,
            data: data,
        });
        userData.update(() => response.data);
        console.log(response.data);
        goto('/');
        // success('you have successfully logged in');
    } catch (e) {
        console.log(e);
        console.log("yo mama");
        // failure('login failed check your username and password');
    }
};


