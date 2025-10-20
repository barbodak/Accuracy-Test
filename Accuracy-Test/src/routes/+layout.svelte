<script lang="ts">
    import "../app.css";
    import axios from "axios";
    import { onMount } from "svelte";
    import { userData } from "$lib/stores/userStore";
    import { tokenExpiryDateTimeValidator } from "$lib/utils/datetime";

    // --- Axios Setup ---
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.interceptors.request.use((config) => {
        const token = $userData?.token;
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    });

    // --- Component Mount Logic ---
    onMount(() => {
        // Persist user data to localStorage
        if (typeof localStorage !== "undefined") {
            const unsubscribe = userData.subscribe((value) => {
                localStorage.setItem("userData", JSON.stringify(value));
            });
        }
        // Check if the auth token has expired
        tokenExpiryDateTimeValidator();
    });
</script>

<!-- This slot will render the content of the current page (e.g., +page.svelte) -->
<slot />
