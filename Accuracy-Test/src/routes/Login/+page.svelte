<script lang="ts">
    import { login } from "$lib/utils/api/authentication";
    let data = {
         username : undefined,
         password : undefined,
    }
    let login_promise : Promise <void>;
    function handleLogin() {
        login_promise = login(data);
    }
</script>


<body>
    <div class="h-screen justify-center flex flex-col items-center bg-gray-200">
        <h1 class="text-4xl"> login page </h1>
        <br>
        <div>
            <form class="space-y-4 "> 
                <label for="login_filed" class="block"> username </label>
                <input type="text" name="username" bind:value={data.username} class="border-2  border-black p-1 rounded-md block">
                <label for="password_filed" class="block"> password </label>
                <input type="password" name="password" bind:value={data.password} class="border-2 border-black p-1 rounded-md block">
                {#await login_promise}
                    <button type="submit" class="bg-blue-500 border-black border-2 p-1 rounded-md block"> ...wating </button>
                {:then}
                    <button on:click={handleLogin} type="submit" class="bg-yellow-500 border-black border-2 p-1 rounded-md block"> Login </button>
                {/await}

            </form>
        </div>
    </div>
</body>
