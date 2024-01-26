import { writable } from "svelte/store";

const storedUserData = typeof localStorage !== 'undefined' ? localStorage.getItem('userData') : null;
export const userData = writable(typeof storedUserData === 'string' && storedUserData !== 'undefined'? JSON.parse(storedUserData): {});
