<script lang="ts">
    import "../app.css";
    import axios from "axios";
    import { onMount } from "svelte";
    import { getCookies } from "$lib/utils/cookies";

    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.interceptors.request.use((config) => {
        const token = getCookies("auth_token");
        console.log(token);
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    });
</script>

<slot />
