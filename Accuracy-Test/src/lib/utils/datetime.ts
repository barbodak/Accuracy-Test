import { get } from "svelte/store";
import { userData } from "../stores/userStore";

export const tokenExpiryDateTimeValidator = () => {
    if (!get(userData).expiry) return;
    const tokenExpiryDateTime = new Date(get(userData).expiry)
    const currentDateTime = new Date();
    if (currentDateTime > tokenExpiryDateTime) {
        userData.update(() => {});
    }
    //console.log("TOKEN " + tokenExpiryDateTime.toString())
    //console.log("CURRENT " + currentDateTime.toString());
};
