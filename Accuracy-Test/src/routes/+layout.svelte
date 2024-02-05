<script lang="ts">
    import type { LayoutData } from "./$types";
    import axios from "axios";
    import { userData } from "$lib/stores/userStore";
    import { onMount } from "svelte";
    import { tokenExpiryDateTimeValidator } from "$lib/utils/datetime";
    import "../app.css";
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.interceptors.request.use((config) => {
        const token = $userData?.token;
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        console.log(config.headers.Authorization);
        return config;
    });
    onMount(async () => {
        if (typeof localStorage !== "undefined") {
            const unsubscribe = userData.subscribe((value) => {
                localStorage.setItem("userData", JSON.stringify(value));
            });
        }
        tokenExpiryDateTimeValidator();
    });
</script>

<slot />
