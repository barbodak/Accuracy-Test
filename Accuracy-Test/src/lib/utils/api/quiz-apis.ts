import axios from "axios";
import { BASE_API_URL } from "../constants";

export const submitAnswer = async (data : any) => { 
    try {
        const url = `${BASE_API_URL}/quiz/submit-answer/${data.quiz_type}/`;
        const response = await axios({
            method: 'put',
            data: data,
            url: url,
        });
        return response.data;
    } catch (error) {
        console.error("Error while submitting answer", error);
    }
}   

export const startQuiz = async (data : any) => {
    try {
        const url = `${BASE_API_URL}/quiz/start-quiz/${data.quiz_type}/`;
        const response = await axios({
            method: 'post',
            data: data,
            url: url,
        }); 
        return response.data;
    } catch (error) {
        console.error("Error while starting quiz", error);
    }
}

export const retreiveQuiz = async (data : any) => {
    try {
        const url = `${BASE_API_URL}/quiz/retrieve/${data.quiz_type}/`;
        const response = await axios({
            method: 'get',
            url: url,
        }); 
        console.log(response);
        return response.data;
    } catch (error) {
        console.error("Error while starting quiz", error);
    }
}

export const retreiveAccount = async () => { 
    try {
        const url = `${BASE_API_URL}/account/retrieve/`;
        const response = await axios({
            method: 'get',
            url: url,
        }); 
        return response.data;
    } catch (error) {
        console.error("Error while fetching quiz options", error);
    }
}
