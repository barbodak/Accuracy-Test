<script lang="ts">
    export let canBeExited: boolean;
    export let isTransparent: boolean;
</script>

<div
    on:click
    role="button"
    class={"w-screen h-screen fixed top-0 left-0 flex justify-center items-center " +
        (isTransparent ? "bg-gray-700 bg-opacity-80" : "")}
>
    <div class="relative flex flex-col justify-center items-center max-w-lg">
        <!-- <button class="absolute right-3 top-2 p-3 rounded-3xl bg-red-800 m-4"> -->
        <!--     x -->
        <!-- </button> -->
        <div
            class={"bg-blue-950 text-white rounded-md flex flex-col justify-center items-center max-w-lg" +
                (canBeExited ? "" : " px-8 py-5")}
        >
            <slot />
        </div>
    </div>
</div>
