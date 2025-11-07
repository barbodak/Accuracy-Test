<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    // Assuming quiz-apis.ts is located in $lib/utils/api/
    import { retreiveAccount, finalize } from "$lib/utils/api/quiz-apis";

    // This holds the data we will send to the backend
    let formData = {
        first_name: "",
        last_name: "",
        age: null as number | null,
        sex: "", // Will be 'M', 'F', or 'O'
    };

    // This holds read-only data from the backend (username, org)
    let accountDetails: { username: string; organization_name: string } | null =
        null;

    let isLoading = true; // Show loading spinner on mount
    let error: string | null = null; // To display submission errors
    let submitPromise: Promise<any>; // For the async button

    onMount(async () => {
        try {
            const account = await retreiveAccount();

            if (account) {
                // IMPORTANT: I'm assuming your `retreiveAccount` endpoint returns
                // a boolean `is_finalized` to indicate if the user has already
                // filled out this form. You must add this to your Django API.
                if (account.is_final) {
                    // User already filled this out, send them to the dashboard
                    await goto("/"); // <-- Or wherever your main app is
                } else {
                    // User needs to fill out the form.
                    // I'm assuming your API returns these fields.
                    accountDetails = {
                        username: account.username,
                        organization_name: account.organization_name,
                    };
                    isLoading = false;
                }
            }
        } catch (e) {
            console.error("Failed to retrieve account:", e);
            await goto("/"); // Send to login on error
        }
    });

    async function handleSubmit() {
        // Simple validation
        if (
            !formData.first_name ||
            !formData.last_name ||
            !formData.age ||
            !formData.sex
        ) {
            error = "Please fill out all fields.";
            return;
        }
        if (formData.age <= 0) {
            error = "Please enter a valid age.";
            return;
        }
        error = null;

        // Call the finalize API

        try {
            const submitPromise = await finalize(formData);
            // Success! Redirect to the dashboard.
            await goto("/"); // <-- Or wherever your main app is
        } catch (e) {
            console.error("Failed to finalize account:", e);
            error = "An error occurred. Please try again.";
        }
    }
</script>

<svelte:head>
    <title>Complete Your Profile</title>
    <style>
        body {
            /* Matches the background from your login +page.svelte */
            background-color: #f1f5f9; /* Slate 100 */
        }
    </style>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-slate-100 p-4">
    {#if isLoading}
        <!-- Simple loading text, you can replace this with a spinner -->
        <div class="text-slate-700">Loading...</div>
    {:else if accountDetails}
        <div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl sm:p-8">
            <h1
                class="mb-4 text-center text-2xl font-bold text-slate-800 sm:text-3xl"
            >
                Complete Your Profile
            </h1>

            <!-- Display read-only info -->
            <div
                class="mb-6 rounded-md border border-slate-200 bg-slate-50 p-4 text-sm"
            >
                <p class="text-slate-700">
                    Welcome, <span class="font-medium text-slate-900"
                        >{accountDetails.username}</span
                    >.
                </p>
                <p class="mt-1 text-slate-600">
                    Organization: <span class="font-medium text-slate-800"
                        >{accountDetails.organization_name}</span
                    >
                </p>
                <p class="mt-3 text-xs text-slate-500">
                    Please fill in your details to continue.
                </p>
            </div>

            <form class="space-y-6" on:submit|preventDefault={handleSubmit}>
                <!-- First Name -->
                <div>
                    <label
                        for="first_name"
                        class="mb-1 block text-sm font-medium text-slate-700"
                    >
                        First Name
                    </label>
                    <input
                        type="text"
                        name="first_name"
                        id="first_name"
                        bind:value={formData.first_name}
                        class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                        placeholder="Jane"
                        required
                    />
                </div>

                <!-- Last Name -->
                <div>
                    <label
                        for="last_name"
                        class="mb-1 block text-sm font-medium text-slate-700"
                    >
                        Last Name
                    </label>
                    <input
                        type="text"
                        name="last_name"
                        id="last_name"
                        bind:value={formData.last_name}
                        class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                        placeholder="Doe"
                        required
                    />
                </div>

                <!-- Age -->
                <div>
                    <label
                        for="age"
                        class="mb-1 block text-sm font-medium text-slate-700"
                    >
                        Age
                    </label>
                    <input
                        type="number"
                        name="age"
                        id="age"
                        min="1"
                        bind:value={formData.age}
                        class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                        placeholder="25"
                        required
                    />
                </div>

                <!-- Sex -->
                <div>
                    <label
                        for="sex"
                        class="mb-1 block text-sm font-medium text-slate-700"
                    >
                        Sex
                    </label>
                    <select
                        name="sex"
                        id="sex"
                        bind:value={formData.sex}
                        class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                        required
                    >
                        <option value="" disabled>Please select...</option>
                        <option value="M">Male</option>
                        <option value="F">Female</option>
                        <option value="O">Other</option>
                    </select>
                </div>

                <!-- Error Message -->
                {#if error}
                    <div
                        class="rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-700"
                    >
                        {error}
                    </div>
                {/if}

                <!-- Submit Button -->
                {#await submitPromise}
                    <button
                        type="submit"
                        disabled
                        class="flex w-full justify-center rounded-lg bg-indigo-400 px-4 py-2.5 text-sm font-medium text-white opacity-75 shadow-sm"
                    >
                        Saving...
                    </button>
                {:then}
                    <button
                        type="submit"
                        class="flex w-full justify-center rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm transition-colors duration-200 hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-indigo-300"
                    >
                        Save and Continue
                    </button>
                {/await}
            </form>
        </div>
    {/if}
</div>
