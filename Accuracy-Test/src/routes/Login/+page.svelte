<script lang="ts">
    // This script block is unchanged from your original.
    import { login } from "$lib/utils/api/authentication";
    let data = {
        username: undefined,
        password: undefined,
    };
    let login_promise: Promise<void>;
    function handleLogin() {
        // Add a simple check to prevent empty submissions
        if (!data.username || !data.password) {
            return;
        }
        login_promise = login(data);
    }
</script>

<svelte:head>
    <style>
        body {
            /* Matches the background from +page.svelte */
            background-color: #f1f5f9; /* Slate 100 */
        }
    </style>
</svelte:head>

<div class="flex min-h-screen items-center justify-center bg-slate-100 p-4">
    <div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl sm:p-8">
        <h1
            class="mb-6 text-center text-2xl font-bold text-slate-800 sm:text-3xl"
        >
            Log In
        </h1>

        <form class="space-y-6" on:submit|preventDefault={handleLogin}>
            <div>
                <label
                    for="username"
                    class="mb-1 block text-sm font-medium text-slate-700"
                >
                    Username
                </label>
                <input
                    type="text"
                    name="username"
                    id="username"
                    bind:value={data.username}
                    class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                    placeholder="your_username"
                    required
                />
            </div>

            <div>
                <label
                    for="password"
                    class="mb-1 block text-sm font-medium text-slate-700"
                >
                    Password
                </label>
                <input
                    type="password"
                    name="password"
                    id="password"
                    bind:value={data.password}
                    class="block w-full rounded-md border-slate-300 p-2.5 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-base"
                    placeholder="••••••••"
                    required
                />
            </div>

            {#await login_promise}
                <button
                    type="submit"
                    disabled
                    class="flex w-full justify-center rounded-lg bg-indigo-400 px-4 py-2.5 text-sm font-medium text-white opacity-75 shadow-sm"
                >
                    Logging in...
                </button>
            {:then}
                <button
                    type="submit"
                    class="flex w-full justify-center rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white shadow-sm transition-colors duration-200 hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-indigo-300"
                >
                    Login
                </button>
            {/await}
        </form>
    </div>
</div>
